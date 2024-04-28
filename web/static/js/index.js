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
}());