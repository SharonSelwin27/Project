// Get the "Get Started" button and add the event listener
document.getElementById("getStartedBtn").addEventListener("click", function() 
{

    // Hide the initial screen content (heading and Get Started button)
    document.querySelector("h1").style.display = "none";
    document.getElementById("getStartedBtn").style.display = "none";
    
    // Show the new selection screen with "Encode" and "Decode" buttons
    document.getElementById("selectionScreen").style.display = "flex";

});
