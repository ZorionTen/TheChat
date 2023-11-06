let chats;
let id;
let isHidden = true;
let socket;
let activity = {
    last_activity: Date.now(),
    timeout: 30000
};
let eel;
let tags;
let username = sessionStorage.getItem("username");
let tagging=false;

async function hidden(state) {
    isHidden = state;
    return isHidden;
}
let init = () => {
    try {
        eel.get_server_ip().then((ip) => {
            eel.log("Connecting to server " + ip);
            socket = io(`${ip}`);
            socket.on('error', function () {
                document.write("Sorry, there seems to be an issue with the connection!");
            })
            socket.emit("command", "history", (e) => {
                showMessages(e);
            });
            socket.emit('user_info', { name: username })
            // LISTENERS
            socket.on("message", function (data) {
                showMessages(data);
            });

            socket.on("command", (data) => {
                if (data.hasOwnProperty("data")) {
                    if (data.data.hasOwnProperty("ip")) {
                        id = data.data.ip;
                    } else if (data.data.hasOwnProperty("members")) {
                        let mems = document.querySelector("#mems");
                        mems.innerHTML = "";
                        for (let i of data.data.members) {
                            mems.innerHTML += `<span>${i.name}</span>`;
                        }
                    }
                }
            });
            socket.on("edited", (data) => {
                document.querySelector(
                    `span[data-id="${data.uid}"]`
                ).innerHTML = data.text;
            });

            socket.on("deleted", (data) => {
                document
                    .querySelector(`p[data-id="${data.uid}"]`)
                    .parentElement.remove();
            });

            document.querySelector('#input').addEventListener('transitionend', (e) => {
                toBottom();
            })

            checkUpdate();
            setInterval(checkUpdate, 12 * 3600000);
        });
    } catch ({ name, msg }) {
        if (name == "ReferenceError") {
            console.log(`No eel, You're fucked`);
            alert('Fatal error: [NO EEL]');
        }
    }
    chats = document.querySelector("#chats");
    document.querySelector("#inp_name").innerHTML = username;
    document
        .querySelector("#input textarea")
        .addEventListener("keypress", (e) => {
            if (e.key == "Enter" && !e.shiftKey) {
                e.preventDefault();
                let text = e.target.value;
                let reply_to = "";
                try {
                    reply_to = document.querySelector("#quote .uid").innerHTML;
                } catch { }
                if (text.length < 1) {
                    return true;
                }
                e.target.value = "";
                clearQuote();
                socket.emit("message", {
                    text: text,
                    name: username,
                    reply: reply_to,
                });
            } else if (e.key == "@") {
                show_tags();
            }
            if (tagging) {
                if (e.key = "ArrowDown") {
                    console.log('dpwn');
                } else if (e.key = 'ArrowUp') {
                    console.log('up');
                }
            }
        });
    // AFK check
    document.addEventListener('keypress', activate);
    document.addEventListener('mousemove', activate);

    // Prepare tags_menu
    tags = document.querySelector('tags_menu');
    tags.style = { 'display': "none", "opacity": "0" };
}; // Close init
let showTags = () => {
    tagging = true;
    tags.style.display="block";
    tags.style.opacity="1";

}
let activate = (e) => {
    activity.last_activity = Date.now();
}

function showMessages(msgs) {
    for (let i of msgs) {
        let child = document.createElement("div");
        child.classList.add("message");
        let p = document.createElement('p');
        p.setAttribute("data-id", i.uid);
        p.classList.add('message_p');
        p.innerHTML = `<span class='from'>${i.name} - ${i.from}</span>`;
        if (i.hasOwnProperty("reply") && i.hasOwnProperty("reply_text")) {
            p.innerHTML += `<span class='reply'>${i.reply_text}</span><i class="ri-reply-line"></i></span>`;
        }
        p.innerHTML += `<span class='text'>${htmlEnc(i.text)}</span>`;
        let opts = document.createElement("div");
        opts.classList.add("opts");
        opts.innerHTML = `<button class='opt_btn' onclick='reply("${i.uid}")'><i class="ri-reply-fill"></i></button>`;
        if (id == i.from) {
            child.classList.add("me");
            opts.innerHTML += `
            <button class='opt_btn' onclick='edit(this,"${i.uid}")'><i class="ri-edit-line"></i></button>
            <button class='opt_btn' onclick='del_msg("${i.uid}")'><i class="ri-close-circle-line"></i></button>
            `;
        }
        p.addEventListener("click", () => {
            document.querySelector(`p[data-id='${i.reply}']`).scrollIntoView();
        });
        child.appendChild(p);
        child.appendChild(opts);
        chats.append(child);
    }
    if (msgs.length == 1) {
        notify("New Message", `${msgs[0].name}: ${msgs[0].text.substring(0, 15)}`)
    } else {
        let froms = msgs.map((msg) => msg.name).join(", ");
        notify("New Messages", `from ${froms.substring(0, 15)}...`);
    }
    toBottom();
}

function htmlEnc(s) {
    let new_txt = s
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/'/g, "&#39;")
        .replace(/"/g, "&#34;")
        .replace("\\n", "<br>");
    return new_txt;
}

function toBottom() {
    chats.scrollTo(0, chats.scrollHeight);
}

function notify(title, text) {
    try {
         if((activity.last_activity + activity.timeout) < Date.now()){
            eel.visible(false);
         }
        eel.send_notify(text);
    } catch ({ name, msg }) {
        if (name == "ReferenceError") {
            console.log(`Notification ${text}`);
        }
    }
}

window.addEventListener("pywebviewready", function () {
    console.log("ready");
    eel = pywebview.api;
    init();
});

function edit(elem, uid) {
    let xp = elem.parentElement.parentElement.getElementsByClassName("text")[0];
    xp.setAttribute("contentEditable", true);
    xp.setAttribute("tabindex", "0");
    xp.focus();
    xp.addEventListener("keypress", (e) => {
        if (e.key == "Enter" && !e.shiftKey) {
            e.preventDefault();
            e.target.setAttribute("contentEditable", false);
            e.target.blur();
            socket.emit(
                "edit",
                { uid: uid, text: e.target.innerHTML },
                (e) => { }
            );
        }
    });
    xp.addEventListener("focusout", (e) => {
        e.target.setAttribute("contentEditable", false);
        e.target.setAttribute("tabindex", "None");
        socket.emit("edit", { uid: uid, text: e.target.innerHTML }, (e) => { });
    });
}

function del_msg(uid) {
    socket.emit("delete", { uid: uid });
}

function checkUpdate() {
    socket.emit("update", {}, (data) => {
        if (data.update) {
            eel.log("Updating...");
            eel.update_client(data.url);
        } else {
            eel.log("no update");
        }
    });
}

function reply(uid) {
    let elem = document.querySelector(`p[data-id='${uid}']`);
    let from = elem.getElementsByClassName("from")[0].innerHTML;
    let text = elem.getElementsByClassName("text")[0].innerHTML;
    let str = `<pre>${from}: ${text}</pre>`;
    str = '<span onclick="clearQuote()">x</span>' + str;
    str += `<span class='hidden uid'>${uid}</span>`;
    document.querySelector("#quote").innerHTML = str;
    document.querySelector("#quote").style.display = "block";
    document.querySelector("#msg_input").focus();
}

function clearQuote() {
    document.querySelector("#quote").innerHTML = "";
    document.querySelector("#quote").style.display = "none";
}
