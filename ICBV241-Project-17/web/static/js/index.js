(function(){
    var user_id = 0;

    function get_uid(){
        if(user_id != 0)
            return;
        fetch('/get-uid').then(function(response){
            return response.json()}
        ).then(function(json){
            user_id = json["uid"];
        });
    }

    get_uid();

     function addNameToList(name) {
        const list = document.getElementById('nameList');
        const listItem = document.createElement('li');
        listItem.textContent = name;
        list.appendChild(listItem);
    }

    function highlightSelected() {
        const selectedName = document.querySelector('.selected-name option:selected');
        if (selectedName) {
            selectedName.classList.add('highlighted');  // Add "highlighted" class
        }
        const previouslySelected = document.querySelector('.selected-name.highlighted');
        if (previouslySelected) {
            previouslySelected.classList.remove('highlighted');  // Remove from previous selection
        }
}
}());