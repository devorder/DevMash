// get search form and page links
let searchForm = document.querySelector('#search-form')
let pageLinks = document.querySelectorAll('.page-link')

// ensure search form exists
if(searchForm){
    for(let i = 0; pageLinks.length > i; i++){
        pageLinks[i].addEventListener('click', function(e) {
            e.preventDefault();
            // get data attribute
            page = this.dataset.page;
            // add hidden search input to form
            searchForm.innerHTML += `<input value=${page} type="hidden" name="page"/>`;
            // submit form
            searchForm.submit()
        });
    }
}