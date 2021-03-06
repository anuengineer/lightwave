#include <dce/rpc.h>
#include <dce/dcethread.h>
#include <srp_verifier_h.h>

#define DO_RPC(rpc_pfn, sts) \
  do {                       \
    dcethread_exc *exc;      \
    DCETHREAD_TRY            \
    {                        \
      exc = NULL;            \
      (sts) = rpc_pfn;       \
    }                        \
    DCETHREAD_CATCH_ALL(exc) \
    {                        \
      sts = dcethread_exc_getstatus(exc); \
    }                        \
    DCETHREAD_ENDTRY         \
  } while (0)

long cli_rpc_srp_verifier_new(
    handle_t hServer,
    long alg,
    long ng_type,
    char *username,
    const unsigned char *bytes_A, int len_A,
    const unsigned char **bytes_B, int *len_B,
    const unsigned char **bytes_s, int *len_s,
    const unsigned char **MDA_value, int *MDA_value_len,
    char *n_hex,
    char *g_hex,
    srp_verifier_handle_t *hSrp);

long cli_rpc_srp_verifier_get_session_key(
    handle_t hServer,
    srp_verifier_handle_t hSrp,
    const unsigned char **ret_key,
    int *ret_key_len);

long cli_rpc_srp_verifier_get_session_key_length(
    handle_t hServer,
    srp_verifier_handle_t hSrp,
    long *key_length);

long cli_rpc_srp_verifier_verify_session(
        handle_t hServer,
        srp_verifier_handle_t hSrp,
        const unsigned char *user_M, int user_M_len,
        const unsigned char **bytes_HAMK, int *bytes_HAMK_len);

long cli_rpc_srp_verifier_delete(
        handle_t hServer,
        srp_verifier_handle_t *phSrp);
