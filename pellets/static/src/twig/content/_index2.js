function run_sparkline() {
        $('.sparkline-data').text('').sparkline('html', {
          width: '100%',
          height: 20,
          lineColor: gray,
          fillColor: false,
          tagValuesAttribute: 'data-value'
        })
      }
      // Run sparkline on document view (window) resized
      App.resize(() => {
        run_sparkline()
      })()
      // Run sparkline on sidebar updated (toggle collapse)
      document.addEventListener('sidebar:update', () => {
        run_sparkline()
      })

      // Chart options
      const options = {
        maintainAspectRatio: false, // disable the maintain aspect ratio in options then it uses the available height
        tooltips: {
          mode: 'index',
          intersect: false, // Interactions configuration: https://www.chartjs.org/docs/latest/general/interactions/
        },
        elements: {
          rectangle: {
            borderWidth: 1 // bar border width
          },
          line: {
            borderWidth: 1 // label border width
          }
        }
      }

      // Monthly Sales
      new Chart('monthlySalesChart', {
        type: 'line',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
          datasets: [
            {
              label: 'Last year',
              backgroundColor: Chart.helpers.color(gray).alpha(0.1).rgbString(),
              borderColor: gray,
              fill: 'start',
              data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
              label: 'This year',
              backgroundColor: Chart.helpers.color(blue).alpha(0.1).rgbString(),
              borderColor: blue,
              fill: 'start',
              data: [28, 48, 40, 19, 86, 27, 90]
            }
          ]
        },
        options: options
      })

      // Sales Revenue Map
      $('#vmap').vectorMap({
        map: 'usa_en',
        showTooltip: true,
        backgroundColor: '#fff',
        color: '#d1e6fa',
        colors: {
          fl: blue,
          ca: blue,
          tx: blue,
          wy: blue,
          ny: blue
        },
        selectedColor: '#00cccc',
        enableZoom: false,
        borderWidth: 1,
        borderColor: '#fff',
        hoverOpacity: .85
      })

      // Today Sales
      options.scales= {
        xAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
      new Chart('barChart2', {
        type: 'horizontalBar',
        data: {
          labels: ['6am', '10am', '1pm', '4pm', '7pm', '10pm'],
          datasets: [
            {
              label: 'Today',
              backgroundColor: Chart.helpers.color(cyan).alpha(0.3).rgbString(),
              borderColor: cyan,
              data: [20, 60, 50, 45, 50, 60]
            },
            {
              label: 'Yesterday',
              backgroundColor: Chart.helpers.color(yellow).alpha(0.3).rgbString(),
              borderColor: yellow,
              data: [10, 40, 30, 40, 55, 25]
            }
          ]
        },
        options: options
      })

      // Reload card event
      document.querySelector('#transaction-history').addEventListener('card:reload', function () {
        var thisCard = this
        // reload transaction history...
        setTimeout(() => { // do nothing for a second (this is only for demo)
          App.stopCardLoader(thisCard) // when done, run this function
        }, 1000)
      })
      document.querySelector('#new-customers').addEventListener('card:reload', function () {
        var thisCard = this
        // reload new customers..
        setTimeout(() => { // do nothing for a second (this is only for demo)
          App.stopCardLoader(thisCard) // when done, run this function
        }, 1000)
      })
      document.querySelector('#today-sales').addEventListener('card:reload', function () {
        var thisCard = this
        // reload today sales..
        setTimeout(() => { // do nothing for a second (this is only for demo)
          App.stopCardLoader(thisCard) // when done, run this function
        }, 1000)
      })