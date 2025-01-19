document.addEventListener('DOMContentLoaded', function () {
    students = document.querySelectorAll(".child-name");
    students.forEach(element => {
        const initial_display = element.nextElementSibling.style.display;
        element.nextElementSibling.style.display = "none";
        element.addEventListener("click", function (e) {
            const content = e.target.nextElementSibling;
            if (content.style.display === "none") {
                content.style.display = initial_display;
            }
            else {
                content.style.display = "none";
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