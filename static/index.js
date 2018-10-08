
var LABELS = {
	"clean": {
		"title": "The lab is clean!",
		"description": "Just look how it sparkles"
	},
	"messy": {
		"title": "The lab is messy!",
		"description": "Time for some cleaning"
	},
	"busy": {
		"title": "The lab is busy!",
		"description": "Look at all those people having fun"
	}
};

function setLabel(label) {
	document.getElementById("title").innerHTML = label.title;
	document.getElementById("description").innerHTML = label.description;
}

function handleResult(result) {
	document.getElementById("result").innerHTML = JSON.stringify(result);
	var max = result.clean;

	if (result.messy > max) {
		max = result.messy;
	}
	if (result.busy > max) {
		max = result.busy;
	}

	switch (max) {
		case result.clean:
			setLabel(LABELS.clean);
			break;
		case result.messy:
			setLabel(LABELS.messy);
			break;
		case result.busy:
			setLabel(LABELS.busy);
			break;
	}
}

function pictureTaken() {
	// Reload picture
	console.log("Updating picturee");
	lab_image = document.getElementById("lab-image");
	lab_image.src = "lab.jpg";
}

function takePicture() {
	console.log("Requesting new picture");
	var xhr = new XMLHttpRequest();
	xhr.timeout = 0;
	xhr.addEventListener("load", pictureTaken);
	xhr.open("GET", "./take-picture");
	xhr.send();
	lab_image = document.getElementById("lab-image");
	lab_image.src = "";
}

function onInitialResult() {
  console.log(this.responseText);
  handleResult(JSON.parse(this.responseText));
}

function getResult() {
	console.log("Getting initial result");
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load", onInitialResult);
	xhr.open("GET", "./result");
	xhr.send();
}

window.onload = function() {
	getResult();
	var es = new EventSource("/subscribe");

	es.onmessage = function (event) {
		console.log(event.data);
		handleResult(JSON.parse(event.data));
	};
};
