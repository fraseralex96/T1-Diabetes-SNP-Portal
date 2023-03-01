//This javascript code allows the user to select/deselect all checkboxes in a list.


//function to select all checkboxes using button// 
function selectAll(){
    var snps=document.getElementsByName('ld'); /*creates variable named snps and assigns the elements that have name 'ld' to it (all the checkboxes)*/
    for(var i=0; i<snps.length; i++){ //loops through the same number of checkboxes there are
        if(snps[i].type=='checkbox') //if a checkbox is present 
            snps[i].checked=true; //check the box
    }
}

//function to deselct all checkboxes using button
function deselectAll(){
    var snps=document.getElementsByName('ld');
    for(var i=0; i<snps.length; i++){
        if(snps[i].type=='checkbox') //if a checkbox is present 
            snps[i].checked=false; //uncheck the box
    }
}      