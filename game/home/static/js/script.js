//Pop ups for certain events
function saveMessage() {
    alert("Save successful!");
}

function amounterror(currency) {
    alert("Not enough " + currency + " for this transaction!");
}

function packagesuccess() {
    alert("Package successfully bought!");
}

function summonerror() {
    alert("Not enough space in inventory for new characters!");
}

function allrewardsclaimed() {
    alert("Rewards successfully claimed!");
}

function rewardclaimed() {
    alert("Reward successfully claimed!");
}

function releasesuccess() {
    alert("Character successfully released!");
}

//Toggles password
function togglepassword() {
    var visibility;
    visibility = document.getElementById("passwordtext");
    if (visibility.type === "text") {
        visibility.type = "password";
        icon = document.getElementById("eyeicon");
        icon.classList.remove("bi", "bi-eye");
        icon.classList.add("bi", "bi-eye-slash");
        
    }
    else {
        visibility.type = "text";
        icon = document.getElementById("eyeicon");
        icon.classList.remove("bi", "bi-eye-slash");
        icon.classList.add("bi", "bi-eye");
    }
}

//Provides content for tabs
function displayitemlist(event, packagetype) {
    var i, itemlist, tabs;
    itemlist = document.getElementsByClassName("itemlist");
    for (i = 0; i < itemlist.length; i++) {
        itemlist[i].style.display = "none";
    }
    tabs = document.getElementsByClassName("tabs");
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    document.getElementById(packagetype).style.display = "block";
    event.currentTarget.className += " active";
    getdefault(packagetype);

}

//Retrieves tab that is active
function getdefault(tabname) {
    document.getElementById("defaultname").value = tabname;
}

//Makes the summoned characters appear one by one
function showslowly(index) {
    summon = document.getElementsByClassName("summons");
    if (index < summon.length) {
        summon[index].style.opacity = 1;
        setTimeout(() => showslowly(index + 1), 500);
    }
}