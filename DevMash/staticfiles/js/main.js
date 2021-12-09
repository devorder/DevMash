// get search form and page links
let searchForm = document.querySelector('#search-form')
let pageLinks = document.querySelector('.page-link')

// ensure search form exists
if(searchForm){
    for(i = 0; pageLinks > i; i++){
        pageLinks[i].addEventListener('click', (e) => {
            e.preventDefault();
            console.log("Button Clicked");
        });
    }
}