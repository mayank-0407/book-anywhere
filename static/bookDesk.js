function bookDesk(desk_id){
    document.getElementById("Unique_id").value = desk_id;
}

const today = new Date()
const day_after_tom = new Date(today)
day_after_tom.setDate(day_after_tom.getDate() + 2)

document.getElementById("from_").min = today.toISOString().split("T")[0];
document.getElementById("from_").max = day_after_tom.toISOString().split("T")[0];

document.getElementById("to_").min = today.toISOString().split("T")[0];
document.getElementById("to_").max = day_after_tom.toISOString().split("T")[0];
