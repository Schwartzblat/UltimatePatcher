#include <jni.h>
#include <string>
#include <cstring>
#include "hook.hpp"

std::unordered_map<std::string, std::pair<ArtMethod*, ArtMethod*>> hooked_methods;


ArtMethod* get_method_id(JNIEnv *env, jclass klass, const char *method_name, const char *method_signature) {
    jmethodID method = env->GetMethodID(klass, method_name, method_signature);
    if (method != nullptr) {
        return (ArtMethod*)method;
    }
    env->ExceptionClear();
    return (ArtMethod*)env->GetStaticMethodID(klass, method_name, method_signature);
}

void switch_art_methods (ArtMethod* method1, ArtMethod* method2) {
    ArtMethod::PtrSizedFields temp_ptr_fields = method1->ptr_sized_fields_;
    method1->ptr_sized_fields_ = method2->ptr_sized_fields_;
    method2->ptr_sized_fields_ = temp_ptr_fields;

#if ANDROID_VERSION < 12
    ArtMethod temp = *method1;
    *method1 = *method2;
    *method2 = temp;
//    uint32_t temp_dex_code_item_offset = method1->dex_code_item_offset_;
//    method1->dex_code_item_offset_ = method2->dex_code_item_offset_;
//    method2->dex_code_item_offset_ = temp_dex_code_item_offset;
//
//    uint32_t declaring_class = method1->declaring_class_;
//    method1->declaring_class_ = method2->declaring_class_;
//    method2->declaring_class_ = declaring_class;
//
//    uint16_t imt_index_ = method1->imt_index_;
//    method1->imt_index_ = method2->imt_index_;
//    method2->imt_index_ = imt_index_;
//
//    uint32_t access_flags = method1->access_flags_;
//    method1->access_flags_ = method2->access_flags_;
//    method2->access_flags_ = access_flags;
//
//    uint32_t dex_method_index = method1->dex_method_index_;
//    method1->dex_method_index_ = method2->dex_method_index_;
//    method2->dex_method_index_ = dex_method_index;
//
//    uint16_t hotness_count_ = method1->hotness_count_;
//    method1->hotness_count_ = method2->hotness_count_;
//    method2->hotness_count_ = hotness_count_;

#endif

}


extern "C"
JNIEXPORT jint JNICALL
Java_com_smali_1generator_TheAmazingPatch_hook_1method(JNIEnv *env, jclass thiz, jstring class_name,
                                              jstring method_name, jstring method_signature,
                                              jobject method) {
    char *class_name_c = (char *) env->GetStringUTFChars(class_name, nullptr);
    char *method_name_c = (char *) env->GetStringUTFChars(method_name, nullptr);
    char *method_signature_c = (char *) env->GetStringUTFChars(method_signature, nullptr);
    jclass klass = env->FindClass(class_name_c);
    if (klass == nullptr) {
        return HOOK_CLASS_NOT_FOUND;
    }
    auto original_method = get_method_id(env, klass, method_name_c, method_signature_c);
    if (original_method == nullptr) {
        return HOOK_ORIGINAL_METHOD_NOT_FOUND;
    }
    jclass callable_class = env->GetObjectClass(method);
    auto call_method = get_method_id(env, callable_class, "call", method_signature_c);
    if (call_method == nullptr) {
        return HOOK_CALL_METHOD_NOT_FOUND;
    }
    hooked_methods[std::string(class_name_c) + std::string(method_name_c) + std::string(method_signature_c)] = std::make_pair(original_method, call_method);
    switch_art_methods(original_method, call_method);
    return HOOK_SUCCESS;
}

extern "C"
JNIEXPORT jint JNICALL
Java_com_smali_1generator_TheAmazingPatch_revert_1hook_1method(JNIEnv *env, jclass thiz, jstring class_name,
                                                       jstring method_name, jstring method_signature) {
    char *class_name_c = (char *) env->GetStringUTFChars(class_name, nullptr);
    char *method_name_c = (char *) env->GetStringUTFChars(method_name, nullptr);
    char *method_signature_c = (char *) env->GetStringUTFChars(method_signature, nullptr);
    std::pair<ArtMethod*, ArtMethod*> methods = hooked_methods[std::string(class_name_c) + std::string(method_name_c) + std::string(method_signature_c)];
    switch_art_methods(methods.first, methods.second);
    return 0;
}
