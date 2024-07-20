
function showTab(tabIndex) {
    var contents = document.getElementsByClassName('content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }
    document.getElementById('content' + tabIndex).style.display = 'block';
}