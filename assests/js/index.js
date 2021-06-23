function changeToFITB() {
    document.getElementById('nat').style.display = 'block';
    document.getElementById('mcq').style.display = 'none';
}

function changeToMCQ() {
    document.getElementById('mcq').style.display = 'block';
    document.getElementById('nat').style.display = 'none';
}

function changeToFITBm() {
    document.getElementById('natm').style.display = 'block';
    document.getElementById('mcqm').style.display = 'none';
    console.log("changeToFITBm")
}

function changeToMCQm() {
    document.getElementById('natm').style.display = 'none';
    document.getElementById('mcqm').style.display = 'block';

    console.log("changeToMCQm")
}