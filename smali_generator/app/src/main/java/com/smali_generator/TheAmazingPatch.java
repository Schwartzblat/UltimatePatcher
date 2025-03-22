package com.smali_generator;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.View;

import java.lang.reflect.Method;
import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicBoolean;


interface CallableVoidOneParameter<T> {
    void call(T t);
}

interface CallableVoidOneParameterBundle {
    boolean call(View view, MotionEvent motionEvent);
}

@SuppressWarnings("unused")
public class TheAmazingPatch {
    static {
        System.loadLibrary("ultimate-patcher");
    }
    public static native int hook_method(String class_name, String method_name, String method_signature, Object callback);
    public static native int revert_hook_method(String class_name, String method_name, String method_signature);


    static CallableVoidOneParameterBundle bundle_callable;
    static AtomicBoolean is_loaded = new AtomicBoolean(false);
    public static void on_load() {
        if (is_loaded.getAndSet(true)) {
            return;
        }
        Log.e("PATCH", "Patch loaded");
        try {
            Class<?> main_activity = Class.forName("com.androbaby.original2048.MainActivity");
            Method onTouch = main_activity.getMethod("onTouch", View.class, MotionEvent.class);
            hook_method("com/androbaby/original2048/MainActivity", "onTouch", "(Landroid/view/View;Landroid/view/MotionEvent;)Z", bundle_callable = (view, motionEvent) -> {
                Log.e("PATCH", "MainActivity.onTouch called: " + view.toString() + ", " + motionEvent.toString());
                revert_hook_method("com/androbaby/original2048/MainActivity", "onTouch", "(Landroid/view/View;Landroid/view/MotionEvent;)Z");
//                boolean ret = TheAmazingPatch.bundle_callable.call(view, motionEvent);
                Display ret = null;
                try {
                    ret = (Display) onTouch.invoke(main_activity, view, motionEvent);
                } catch (Exception e) {
                    Log.e("PATCH", "Error inside: " + e.getMessage());
                }
                revert_hook_method("com/androbaby/original2048/MainActivity", "onTouch", "(Landroid/view/View;Landroid/view/MotionEvent;)Z");
                Log.e("PATCH", "MainActivity.onTouch returned: " + ret);
                return false;
            });
        } catch (Exception e) {
            Log.e("PATCH", "Error: " + e.getMessage());
        }
    }
}