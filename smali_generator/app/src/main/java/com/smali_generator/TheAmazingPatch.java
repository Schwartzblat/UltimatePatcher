package com.smali_generator;

import android.util.Log;
import android.view.View;
import java.util.concurrent.atomic.AtomicBoolean;

class TheAmazingPatch {
    static AtomicBoolean is_loaded = new AtomicBoolean(false);
    public static void on_load(View view) {
        if (is_loaded.getAndSet(true)) {
            return;
        }
        Log.e("PATCH", "Patch loaded");
    }
}