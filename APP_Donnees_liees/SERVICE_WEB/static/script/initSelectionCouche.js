

function creationSelectionCouche(){

	
				
	$( "#osm" ).change(function(){
		layerBase1.setVisible(!layerBase1.getVisible());
		layerBase2.setVisible(!layerBase2.getVisible());
	});
	
	$( "#mqsat" ).change(function(){
		layerBase1.setVisible(!layerBase1.getVisible());
		layerBase2.setVisible(!layerBase2.getVisible());
	});

	$( "#urbain" ).click(function(){
		layer1.setVisible(!layer1.getVisible());
	});
	
	$( "#urbainwfs" ).click(function(){
		layer2wfs.setVisible(!layer2wfs.getVisible());
	});
	
	$( "#ParcArmandDuplessis" ).click(function(){
		layerJSON.setVisible(!layerJSON.getVisible());
	});

	


}


