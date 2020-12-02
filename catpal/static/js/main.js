function moverA(){
    let alluserscheckboxes = document.getElementById("all-users-checks").childNodes;
    let guserschecb = document.getElementById("g-checks");
    //let usersFromGroup = {{group.user_set.get()}};
    for (var el of alluserscheckboxes) {
        if(el.hasChildNodes()){
            for (var el2 of el.childNodes){
                    if (el.type == "checkbox"  && el.checked){
                        guserschecb.appendChild(el.parentNode);
                    }
                }
        }
    }

}
