//
// Created by alon on 3/17/25.
//

#ifndef TEST_HOOK_HPP
#define TEST_HOOK_HPP

#include <jni.h>
#include <pthread.h>
#include <cstdio>
#include <unistd.h>
#include <android/log.h>
#include <vector>
#include <unordered_map>
#include <netinet/in.h>
#include <cstdlib>
#include <cstring>
#include <sys/socket.h>
#include <sys/endian.h>
#include <sys/stat.h>

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, "NODER", __VA_ARGS__)

struct ArtMethod {
    uint32_t declaring_class_;

    // Access flags; low 16 bits are defined by spec.
    // Getting and setting this flag needs to be atomic when concurrency is
    // possible, e.g. after this method's class is linked. Such as when setting
    // verifier flags and single-implementation flag.
    uint32_t access_flags_;

    /* Dex file fields. The defining dex file is available via declaring_class_->dex_cache_ */
#if ANDROID_VERSION < 12
    // Offset to the CodeItem.
    uint32_t dex_code_item_offset_;
#endif

    // Index into method_ids of the dex file associated with this method.
    uint32_t dex_method_index_;

    /* End of dex file fields. */


    // Entry within a dispatch table for this method. For static/direct methods the index is into
    // the declaringClass.directMethods, for virtual methods the vtable and for interface methods the
    // interface's method array in `IfTable`s of implementing classes.
    uint16_t method_index_;

    union {
        // Non-abstract methods: The hotness we measure for this method. Not atomic,
        // as we allow missing increments: if the method is hot, we will see it eventually.
        uint16_t hotness_count_;
        // Abstract methods: IMT index.
        uint16_t imt_index_;
    };

    // Fake padding field gets inserted here.

    // Must be the last fields in the method.
    struct PtrSizedFields {
        // Depending on the method type, the data is
        //   - native method: pointer to the JNI function registered to this method
        //                    or a function to resolve the JNI function,
        //   - resolution method: pointer to a function to resolve the method and
        //                        the JNI function for @CriticalNative.
        //   - conflict method: ImtConflictTable,
        //   - abstract/interface method: the single-implementation if any,
        //   - proxy method: the original interface method or constructor,
        //   - default conflict method: null
        //   - other methods: during AOT the code item offset, at runtime a pointer
        //                    to the code item.
        void* data_;

        // Method dispatch from quick compiled code invokes this pointer which may cause bridging into
        // the interpreter.
        void* entry_point_from_quick_compiled_code_;
    } ptr_sized_fields_;
};


enum HookResult{
    HOOK_SUCCESS,
    HOOK_CLASS_NOT_FOUND,
    HOOK_ORIGINAL_METHOD_NOT_FOUND,
    HOOK_CALL_METHOD_NOT_FOUND,
};

#endif //TEST_HOOK_HPP
