document.addEventListener('DOMContentLoaded', function () {
    students = document.querySelectorAll(".child-name");
    students.forEach(element => {
        const initial_display = element.nextElementSibling.style.display;
        const initial_display_next = element.nextElementSibling.nextElementSibling.style.display;
        element.nextElementSibling.style.display = "none";
        element.nextElementSibling.nextElementSibling.style.setProperty("display", "none", "important");
        element.addEventListener("click", function (e) {
            const content = e.target.nextElementSibling;
            const content_next = e.target.nextElementSibling.nextElementSibling;
            if (content.style.display === "none") {
                content.style.display = initial_display;
                content_next.style.display = initial_display_next
            }
            else {
                content.style.display = "none";
                content_next.style.setProperty("display", "none", "important");
            }
        });

    });
    // document.querySelector(".child-name").addEventListener("click", function (e) {
    //     const content = e.target.nextElementSibling.style;
    //     if (content.display === "grid") {
    //         content.display = "none";
    //     }
    //     else {
    //         content.display = "grid";
    //     }
    // });
});