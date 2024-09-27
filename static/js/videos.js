$(document).ready(function() {
    // Search functionality
    $('#search').on('input', function() {
        const searchValue = $(this).val().toLowerCase();
        $('.video-item').each(function() {
            const title = $(this).find('.card-title').text().toLowerCase();
            $(this).toggle(title.includes(searchValue));
        });
    });

    // Sort functionality
    $('#sort').on('change', function() {
        const sortValue = $(this).val();
        const videoList = $('#video-list');
        const videos = videoList.children('.video-item');

        videos.sort(function(a, b) {
            const dateA = new Date($(a).find('.card-text').text().replace('Uploaded on: ', ''));
            const dateB = new Date($(b).find('.card-text').text().replace('Uploaded on: ', ''));

            return sortValue === 'latest' ? dateB - dateA : dateA - dateB;
        });

        videoList.append(videos);
    });
});
