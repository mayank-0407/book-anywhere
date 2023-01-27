let main_id
function mdesk(desk_id,desk_zone,desk_mCount,desk_status){
    document.getElementById("zone_id").value = desk_zone;
    document.getElementById("deskcount_id").value = desk_mCount;
    document.getElementById("status_id").value = desk_status;
    main_id=desk_id
}

function sendReqToServer(statuss, zone ,monitorCount,id){

    
    serializedData={'statuss' : statuss, 'desk_id':id,'zone' : zone, 'monitorCount' : monitorCount};
    console.log(serializedData);
    

    $.ajax({
        type: 'GET',
        url: "./submit",
        data: serializedData,
        success: function (response) {
            console.log("Desk has been updated.")
            location.reload()
        },
        error: function (response) {
            location.reload()
            alert(response["responseJSON"]["error"]);
        }
    })
}

submit_edit.addEventListener('click', ()=>{

    statuss=document.getElementById('status_id').value;
    console.log(statuss)
    zone=document.getElementById('zone_id').value;
    monitorCount=document.getElementById('deskcount_id').value;
    sendReqToServer(statuss, zone ,monitorCount,main_id);
})