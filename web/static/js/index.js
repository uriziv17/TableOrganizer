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
}());