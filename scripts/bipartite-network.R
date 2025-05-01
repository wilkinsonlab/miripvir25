# Load necessary library
# Suppress warnings and messages
options(warn = -1)
suppressMessages({
  library(optparse)
  library(bipartite)
  library(parallel)
})
# Define command line options
option_list <- list(
    make_option(c("-f", "--file"), type = "character", default = NULL,
                            help = "Input file path", metavar = "character"),
    make_option(c("-r", "--repetitions"), type = "integer", default = 1,
                            help = "Number of repetitions", metavar = "integer"),
    make_option(c("-o", "--output"), type = "character", default = NULL,
                            help = "Output file path", metavar = "character")
)

# Parse command line arguments
opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

# Check if required arguments are provided
if (is.null(opt$file) || is.null(opt$output)) {
    stop("Both input file and output file must be specified. Use --help for more information.")
}

# Print parsed arguments (for debugging purposes)
cat("Input file:", opt$file, "\n")
cat("Repetitions:", opt$repetitions, "\n")
cat("Output file:", opt$output, "\n")


u <- read.csv(opt$file, header = TRUE, row.names = 1, sep=";")

# 1. Calculate observed metrics
observed <- networklevel(u, index = c("NODF", "connectance", "modularity"))

# 2. Create null models (100 iterations for speed - increase for final run)
# null_models <- nullmodel(u, N=opt$repetitions, method="r2d")

n_cores <- detectCores() - 1  # Use all but one core
cat("Using", n_cores, "cores for parallel processing.\n")

cl <- makeCluster(n_cores)
clusterExport(cl, varlist = c("u", "networklevel", "nullmodel"))

# 3. Calculate metrics for null models

nulls <- parLapply(cl, 1:opt$repetitions, function(i) {
  nm <- nullmodel(u, N = 1, method = "r2d")[[1]]
  networklevel(nm, index = c("NODF", "connectance", "modularity"))
})
stopCluster(cl)
null_results <- do.call(rbind, nulls)

# 4. Save results to CSV files
write.csv(data.frame(Metric = names(observed), Value = observed),
          paste(opt$output, "observed.csv", sep="."), row.names = FALSE)

write.csv(null_results, paste(opt$output, "null.csv", sep="."), row.names = FALSE)
