

// Fonctions du menu
function infoMenu() {
	var title = document.getElementById("title");
	title.innerHTML = "Informations";
	var parcname = document.getElementById("parcname");
	parcname.innerHTML = "Sélectionnez un parc";
	var content = document.getElementById("content");
	content.innerHTML = "";
  }
  
  function layersMenu() {
	var title = document.getElementById("title");
	title.innerHTML = "Couches";
	var parcname = document.getElementById("parcname");
	parcname.innerHTML = "Sélectionnez un parc";
	var content = document.getElementById("content");
	content.innerHTML = "";
  }
  
  function legendMenu() {
	var title = document.getElementById("title");
	title.innerHTML = "Légende";
	var parcname = document.getElementById("parcname");
	parcname.innerHTML = "Sélectionnez un parc";
	var content = document.getElementById("content");
	content.innerHTML = "";
  }
  
  function baseLayersMenu() {
	var title = document.getElementById("title");
	title.innerHTML = "Fonds de carte";
	var parcname = document.getElementById("parcname");
	parcname.innerHTML = "Sélectionnez un parc";
	var content = document.getElementById("content");
	content.innerHTML = "";
  }
  
  function helpMenu() {
	var title = document.getElementById("title");
	title.innerHTML = "A propos";
	var parcname = document.getElementById("parcname");
	parcname.innerHTML = "Sélectionnez un parc";
  
	var content = document.getElementById("content");
	content.innerHTML = "";
  }
  
  function hideMenu() {
	var menu = document.getElementById("menu");
	menu.hidden = !menu.hidden;
  }
  
  // Onglets Info
  var topobutton = document.getElementById("topobutton");
  topobutton.addEventListener("click", topoMenu);
  
  var parcbutton = document.getElementById("parcbutton");
  parcbutton.addEventListener("click", parcMenu);
  
  var otherbutton = document.getElementById("otherbutton");
  otherbutton.addEventListener("click", otherMenu);
  
  function topoMenu() {
	content1.hidden = false;
	content2.hidden = true;
	content3.hidden = true;
	othercontent.hidden = true;
  }
  
  function parcMenu() {
	content1.hidden = true;
	content2.hidden = false;
	content3.hidden = true;
	othercontent.hidden = true;
  }
  
  function otherMenu() {
	content1.hidden = true;
	content2.hidden = true;
	content3.hidden = false;
	othercontent.hidden = true;
  }
  