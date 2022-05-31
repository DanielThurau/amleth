use std::borrow::Borrow;
use std::cell::RefCell;
use ic_cdk::export::candid;
use ic_cdk_macros::*;
use ic_cdk::println;

pub fn log_prefix() -> String {
    "[amleth] ".into()
}

type MessageStore = Vec<String>;

thread_local! {
    static MESSAGE_STORE: RefCell<MessageStore> = RefCell::default();
}

static mut MESSAGES: Option<Vec<String>> = None;

#[init]
fn init() {
    unsafe {
        MESSAGES = Some(vec![]);
        add_message(MESSAGES.as_mut().unwrap());
    }
}

#[pre_upgrade]
fn pre_upgrade() {
    println!("{}Executing pre_upgrade...", log_prefix());
    unsafe {
        for message in MESSAGES.as_mut().unwrap() {
            println!("{}- Message in state: {}", log_prefix(), message)
        }
    }
    // MESSAGE_STORE.with(|messages| {
    //     let y = messages
    //         .borrow();
    // });
    println!("{}Finished pre_upgrade", log_prefix());
}

#[post_upgrade]
fn post_upgrade() {
    println!("{}Executing post_upgrade...", log_prefix());
    unsafe {
        for message in MESSAGES.as_mut().unwrap() {
            println!("{}- Message in state: {}", log_prefix(), message)
        }
    }
    println!("{}Finished post_upgrade", log_prefix());
}

#[update]
fn add() -> () {
    unsafe {
        let msg = MESSAGES.as_mut().unwrap();
        add_message(msg);
    }
}

#[query]
fn get() -> Vec<String> {
    unsafe {
        let response = MESSAGES.as_ref().unwrap().clone();
        return response;
    }
}

fn add_message(messages: &mut Vec<String>) {
    let message_id = messages.len() + 1;
    messages.push(format!("Message-{}", message_id));
}