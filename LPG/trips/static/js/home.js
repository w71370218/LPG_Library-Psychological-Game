var test_index = 0;

function getScore(){
    var i1 = 0;
    var i2 = 0;
    var i3 = 0;
    var i4 = 0;

    var choice_num = document.querySelectorAll('#test').length;
    console.log(choice_num)

    for (var i = 0; i < choice_num; i++) {
        obj = document.querySelectorAll('#test')[i];
        console.log(obj.checked)
        if (obj.checked == true){
            console.log(obj.value);
            res = [obj.value];
            if (obj.value.length > 1){
                var res = res[0].split(", ");
            }
            console.log(res);
            if (res.includes("1")){
                i1+=1;
            } 
            if (res.includes("2")){
                i2+=1;
            }
            if (res.includes("3")){
                i3+=1;
            }
            if (res.includes("4")){
                i4+=1;
            }
        }
    }
    console.log(i1);
    console.log(i2);
    console.log(i3);
    console.log(i4);

}

