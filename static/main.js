$(document).ready(function() {
    $('#movie-search').on('input', function() {
        var search_term = $(this).val();
        if (search_term.length > 0) {
            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: '/search_movie',
                data: JSON.stringify({'search_term': search_term}),
                success: function(response) {
                    var suggestions = response.suggestions;
                    var suggestionsHtml = '<div>';
                    suggestions.forEach(function(movie) {
                        suggestionsHtml += '<a href="#" class="choice">' + movie + '</a> <br>';
                    });
                    suggestionsHtml += '</div>';
                    $('#suggestions').html(suggestionsHtml);
                }
            });
        } else {
            $('#suggestions').html('');
        }
    });

    $('#suggestions').on('click', '.choice', function(event) {
        event.preventDefault();
        var selectedMovieTitle = $(this).text();
        
        var chosenMovies = JSON.parse($('#chosen-movies').val() || '[]');
        if(chosenMovies.length < 5){
            chosenMovies.push(selectedMovieTitle);
            $('#chosen-movies').val(JSON.stringify(chosenMovies));

            //test card dynamic generation
            var testElem = '<div class="card"> <img class="card-img-top" src="../static/images/banner.png" alt="Card image cap"><div class="card-body"><h5 class="card-title">'
            + selectedMovieTitle + '</h5><p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p></div></div>';
            $('.card-deck').append(testElem);
        }else{
            alert("You have already chosen 5 movies.")
        }
        
    });

    $('#search-form').on('submit', function(event) {
        event.preventDefault();
        var chosenMovies = JSON.parse($('#chosen-movies').val() || '[]');
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/recommend',
            data: JSON.stringify({'chosen_movies': chosenMovies}),
            success: function(response) {
                var recommendations = response.recommendations;
                var recommendationsHtml = '<h2>Recommendations:</h2><ul>';
                recommendations.forEach(function(movie) {
                    recommendationsHtml += '<li>' + movie + '</li>';
                });
                recommendationsHtml += '</ul>';
                $('#recommendations').html(recommendationsHtml);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to get recommendations. Please try again.');
            }
        });
    });

    console.log(ans);

});
