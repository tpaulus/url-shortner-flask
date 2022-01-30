// custom scripts

$("#shorten-form").submit(function(event){
    $.ajax({
        url: "/slug",
        type: "PUT",
        data: JSON.stringify({
            "long_url": $("#long_url").val()
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result){
            console.log(result);

            $("#short_url").val(result['short_url'])
            $("#shorten-form").hide()
            $("#shorten-result-form").show()

            $("#long_url").val("")
        },
        error: function(errMsg) {
            alert(errMsg);
        }
    });
    event.preventDefault();
});

$("#shorten-result-form").submit(function(event){
    $("#shorten-result-form").hide()
    $("#shorten-form").show()

    event.preventDefault();
});

$("#describe-form").submit(function(event){
    $.ajax({
        url: "/slugs/" + $("#describe-form > div > input").val().split("/").pop(),
        type: "GET",
        success: function(result){
            console.log(result);

            $("#describe-slug").val(result['slug'])
            $("#describe-long-url").val(result['long_url'])
            $("#describe-date-created").val(result['date_created'])
            if (result['expires'] == null){
                $("#describe-expires").val("Never")
            } else {
                $("#describe-expires").val(result['expires'])
            }

            if (result['expired'] == null){
                $("#describe-expired").val("False")
            } else {
                $("#describe-expired").val(result['expired'])
            }

            $("#stats-24-hours").html(result['stats']['last_day'])
            $("#stats-7-days").html(result['stats']['last_week'])
            $("#stats-all-time").html(result['stats']['all_time'])

            $("#describe-form").hide()
            $("#describe-result-form").show()

            $("#describe-form > div > input").val("")
        },
        error: function(errMsg) {
            alert(errMsg);
        }
    });
    event.preventDefault();
});

$("#describe-result-form").submit(function(event){
    $("#describe-result-form").hide()
    $("#describe-form").show()

    event.preventDefault();
});

$("#delete-slug").click(function(event){
    if (confirm("Are you sure you want to delete this short url?") == true) {
        $.ajax({
        url: "/slugs/" + $("#describe-slug").val(),
        type: "DELETE",
        success: function(result){
            console.log(result);

            $("#describe-result-form").hide()
            $("#describe-form").show()
        },
        error: function(errMsg) {
            alert(errMsg);
        }
        });
    }

    event.preventDefault();
});
