var App = function($){
    /* VARIABLES GLOBAL TO App */
    var THIS = this;
       
    var init = function(){
       
	   $('#labelFront').on('click', function(event){
		  
		  var modalContainer =  $('#labelFrontPopup');
		  showModal(modalContainer);
		   
	   });
	   
	   $('#labelBack').on('click', function(event){
		   var modalContainer =  $('#labelBackPopup');
		   showModal(modalContainer);
		   
	   });
	   
    }

   // Gallery Modal Popup //
	
	 var showModal = function(modalContainer){
		var modalWidth;
		var modalTop;
		var modalHeight;
	
	var $modalContainer = modalContainer;
		
		//modalWidth = 880;
		modalTop = 30;
		//modalHeight = 450;
		
		
				
		$modalContainer.modal({	
			opacity:80,
			overlayCss: {backgroundColor:'#fff'},
			//maxWidth: modalWidth,
			//maxHeight: modalHeight, 
			autoPosition:'true',
			position:[modalTop,0],
            onClose: function(){
                $.modal.close();

            }
		});
		
		
	}
	


    /***** THIS IS THE CALL THAT STARTS IT ALL *****/
    init();
};
// Instantiate application in $(document).ready()
$(function($){
    window.app = new App($);
});