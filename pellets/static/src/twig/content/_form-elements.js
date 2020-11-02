autosize(document.querySelectorAll('textarea.autosize'))
      App.autowidth()

      const cities = [
        'New York',
        'Los Angeles',
        'Chicago',
        'Houston',
        'Philadelphia',
        'Phoenix',
        'San Antonio',
        'San Diego',
        'Dallas',
        'San Jose',
        'Indianapolis',
        'Jacksonville',
        'San Francisco',
        'Austin',
        'Columbus',
        'Fort Worth',
        'Louisville-Jefferson',
        'Charlotte',
        'Detroit',
        'El Paso',
        'Memphis',
        'Nashville-Davidson',
        'Baltimore',
        'Boston',
        'Seattle',
        'Washington',
        'Denver',
        'Milwaukee',
        'Portland',
        'Las Vegas',
      ]
      autocomplete(document.getElementById('autocompleteExample1'), cities)

      for (const rating of document.querySelectorAll('.input-rating')) {
        starRating(rating)
      }

      duallistbox(document.getElementById('exampleDuallistbox'))

      document.getElementById('blogTitle').addEventListener('input', function () { // slugify on input
        document.getElementById('blogTitleSlug').value =
        slugify(this.value, {
          remove: /[*+~.()'"!:@,]/g, // remove symbols
          lower: true // convert to lowercase
        })
      })
      document.getElementById('blogTitle').dispatchEvent(new Event('input'))
