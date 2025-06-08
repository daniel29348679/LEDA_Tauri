#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::env;
use std::process::{Child, Command};
use std::sync::{Arc, Mutex};
use std::{thread, time::Duration};
fn main() {
    // 使用 Arc<Mutex<Child>> 來跨執行緒共享子程序控制權
    let child_process: Arc<Mutex<Option<Child>>> = Arc::new(Mutex::new(None));

    {
        let child_clone = Arc::clone(&child_process);
        thread::spawn(move || {
            let mut path = env::current_exe().expect("Failed to get current exe path");
            path.pop(); // 移除主程式名稱，取得資料夾路徑
            path.push("leda_app/leda_app.exe"); // 加上相對路徑
            let child = Command::new(path)
                .spawn()
                .expect("Failed to start leda_app.exe");

            // 把 child 記錄下來讓主執行緒可以控制
            *child_clone.lock().unwrap() = Some(child);
        });
    }

    // 使用 Ctrl-C handler 確保即使中斷也能關掉子程序
    {
        let child_clone = Arc::clone(&child_process);
        ctrlc::set_handler(move || {
            if let Some(mut child) = child_clone.lock().unwrap().take() {
                let _ = child.kill();
            }
            std::process::exit(0);
        })
        .expect("Error setting Ctrl-C handler");
    }

    thread::sleep(Duration::from_secs(6));
    app_lib::run();

    // 主程式結束時清理子程序
    if let Some(mut child) = child_process.lock().unwrap().take() {
        let _ = child.kill();
    };
}
