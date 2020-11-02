$('.summernote').summernote({
  height: 306
})

$('.select2').select2({
  width: '100%'
})

flatpickr('.datetimepicker-inline', {
  enableTime: true,
  inline: true
})

document.getElementById('blogTitle').addEventListener('input', function () {
  let permalink = 'blog-title'
  if (this.value != '') {
    permalink = slugify(this.value, {
      remove: /[*+~.()'"!:@,]/g, // remove symbols
      lower: true // convert to lowercase
    })
  }
  permalink = `http://example.com/${permalink}.html`
  ;[...document.querySelectorAll('.permalink-value')].map(el => el.value = permalink)
})
