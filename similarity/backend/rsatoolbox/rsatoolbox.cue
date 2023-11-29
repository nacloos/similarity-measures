package backend
import(
    "strings"
)


// TODO: some methods accept extra input (e.g. noise cov)
_rdm_methods: [
    "euclidean",
    "correlation",
    // TODO: ValueError: descriptor must be a string! Crossvalidationrequires multiple measurements to be grouped
    // "mahalanobis",
    // "crossnobis",
    // "poisson",  // TODO: NaNs in the output
    // "poisson_cv"
]

_compare_methods: [
    "cosine",
    "spearman",
    "corr",
    "kendall",
    "tau-b",
    "tau-a",
    "rho-a",
    "corr_cov",
    "cosine_cov",  
    // "neg_riem_dist"  // numpy.linalg.LinAlgError: The leading minor of order 31 of B is not positive definite. The factorization of B could not be completed and no eigenvalues or eigenvectors were computed.
 ]


// TODO: generate mock data to test the metrics?
// see rsatoolbox tests?


// "rsa rdm-euclidiean compare-tau-b"
// <=> make("rsa", rdm="euclidean", compare="tau-b")
// "rsa rdm-euclidiean compare-corr_cov"
// "cca alpha-0.1"

// TODO: all the variations of rsa?
metric: {
    [string]: #Metric & {
        #path: "similarity.backend.rsatoolbox.rsa.compute_rsa"
        #call_key: null
        #partial: true
        #preprocessing: [#reshape2d]
        #postprocessing: [#arccos, #angular_dist_to_score]
        rdm_method: string
        compare_method: string
    }

    rsa: {
        rdm_method: "euclidean"
        compare_method: "cosine"
    }

    for rdm_method in _rdm_methods {
        for compare_method in _compare_methods {
            // replace "-" with "_" in compare_method ("-" is reserved for separating arguments)
            let name = "rsa-" + rdm_method + "-" + strings.Replace(compare_method, "-", "_", -1)
            
            (name): {
                "compare_method": compare_method
                "rdm_method": rdm_method
            }
        }
    }
}
