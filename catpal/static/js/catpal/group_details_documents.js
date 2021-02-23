//the idea is to get the session variable amount and check the radio button
//according the value of that variable
function grabAmount() {
    var radioGroup = document.getElementsByName('amount');
    window.onload = function (){
        for(element of radioGroup){
            if (element.value != sessionStorage.getItem('amount')){
                element.checked == false;
            }
            else{
                element.checked == true;
            }
        }
    }


}