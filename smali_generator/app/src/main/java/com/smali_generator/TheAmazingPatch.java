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

import lab.galaxy.yahfa.HookMain;


@SuppressWarnings("unused")
public class TheAmazingPatch {
    static AtomicBoolean is_loaded = new AtomicBoolean(false);

    static boolean on_touch_hook(Activity activity, View view, MotionEvent motionEvent) {
        Log.e("PATCH", "MainActivity.onTouch called: " + activity.toString() + ", "  + view.toString() +", " + motionEvent.toString());
        boolean ret = TheAmazingPatch.on_touch_hook_backup(activity, view, motionEvent);
        Log.e("PATCH", "MainActivity.onTouch returned: " + ret);
        return ret;
    }

    static boolean on_touch_hook_backup(Activity activity, View view, MotionEvent motionEvent) {
        return true;
    }

    public static void on_load() {
        if (is_loaded.getAndSet(true)) {
            return;
        }
        Log.e("PATCH", "Patch loaded");
        try {
            Class<?> main_activity = Class.forName("com.androbaby.original2048.MainActivity");
            Method on_touch_hook_method = TheAmazingPatch.class.getDeclaredMethod("on_touch_hook", Activity.class, View.class, MotionEvent.class);
            Method on_touch_backup_method = TheAmazingPatch.class.getDeclaredMethod("on_touch_hook_backup", Activity.class, View.class, MotionEvent.class);
            HookMain.findAndBackupAndHook(main_activity, "onTouch", "(Landroid/view/View;Landroid/view/MotionEvent;)Z", on_touch_hook_method, on_touch_backup_method);
        } catch (Exception e) {
            Log.e("PATCH", "Error: " + e.getMessage());
        }
    }
}