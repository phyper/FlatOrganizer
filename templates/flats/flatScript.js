$(document).ready(function() {
        alert("yes");
        $("#btnSetTaskDone").click(function() {
            alert("YEAH!!!");
            var taskId = $(this).parent.attr("id").val();
            alert(taskId);
            //Use this ID to update this in DB.

            $(".alert").alert();
        });
});
