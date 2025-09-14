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

function clickelement(element) {

}

//Provides tabs for shop
function displaypackagelist(event, packagetype) {
    var i, packagelist, tabs;
    packagelist = document.getElementsByClassName("packagelist")
    for (i = 0; i < packagelist.length; i++) {
        packagelist[i].style.display = "none";
    }
    tabs = document.getElementsByClassName("tabs")
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    document.getElementById(packagetype).style.display = "block";
    event.currentTarget.className += " active";

}