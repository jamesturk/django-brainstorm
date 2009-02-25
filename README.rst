

---------------
Creating Themes
---------------

A theme is represented by a single django template, currently kept at templates/themes/themename.html

Required Elements
-----------------

The theme must include a content block that will be filled by the page, the theme should also include "idea_form.html" if you wish to use the generic idea submission form.

Example dynamic content block:
    <!-- content -->
    <div>
        <h2 id="secondLogo"><a href="http://mysite.com/subsite/">{{subsite.name}}</a></h2>
        <div id="featureBox">
            <p>project description</p>
        </div>

        <div id="ltColumn">
        {% block content %}
        {% endblock %}
        </div>

        <div id="rtColumn">
        <h3>Submit New Idea</h3>
            {% include "idea_form.html" %}
        </div>
        <div class="clear"></div>
    </div>


Styling the Theme
-----------------

Obviously the styling/design of the static portions of the theme is entirely within the hands of the designer.  
There are however a few dynamic sections which typically will need some form of styling.

index
.....

The 'content' block of the index contains two divs: 'div#ideas' and 'div#pagination'.

'div#ideas' contains an list where each li is a pair of div.btnVote and div.voteContent. When a div.btnVote has been voted up it will have the additional class 'voted' to allow for additional styling.

'div.btnVote' contains the link 'a.vote_link' for voting and 'div.votes_counted' for displaying the current vote total.

'div.voteContent' contains an <h3> with the idea title, a div.commentMeta with the idea's submitter/date, and a <p> with the description.


idea
....

The content block of the idea page contains two divs: 'div#idea' and 'div#comments'.

'div#idea' contains a single pair of 'div.btnVote' and 'div.voteContent' (see `index`_ for description of these elements)

'div#comments' contains an <h3> with the number of comments, then an ordered list where each <li> has the following elements:

* div.commentMeta which contains span.commentMetaAuthor and span.commentMetaDate
* div.commentContent which contains a <p> with the comment itself

(TODO: comment form)
