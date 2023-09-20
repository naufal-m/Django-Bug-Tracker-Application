$(document).ready(function () {
        $('.view-project').click(function () {
            var projectId = $(this).data('project-id');
            var projectName = $(this).data('project-name');
            var projectCode = $(this).data('project-code');
            var createdUser = $(this).data('created-user');
            var assignedUsers = $(this).data('assigned-user');
            var projectDescription = $(this).data('description');

            $('#projectName').text(projectName);
            $('#projectCode').text(projectCode);
            $('#createdUser').text(createdUser);
            $('#assignedUsers').text(assignedUsers);
            $('#projectDescription').text(projectDescription);
        });
    });

    story$(document).ready(function () {
        $('.view-story').click(function () {
            var storyId = $(this).data('story-id');
            var storyName = $(this).data('story-name');
            var storyCode = $(this).data('story-code');
            var createdUser = $(this).data('created-user');
            var assignedUsers = $(this).data('assigned-user');
            var storyDescription = $(this).data('description');

            $('#storyName').text(storyName);
            $('#projectCode').text(storyCode);
            $('#createdUser').text(createdUser);
            $('#assignedUsers').text(assignedUsers);
            $('#storyDescription').text(storyDescription);
        });
    });