#Written by Daniel O'Neill for Eventbrite internship interview
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, QueryDict
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from urllib import urlopen, quote_plus
import json
import datetime
from events.models import Category
from django.contrib.staticfiles.templatetags.staticfiles import static


class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.order_by('cat_id')

#Initial Category loading view
#it gets called if the Category model is not populated
#when the index page is reached (first run)
def cats(request):
    cat_req = urlopen("https://www.eventbriteapi.com/v3/categories/?token=A3KV5OGJFN7YWZI6JLIC")
    json_in = cat_req.read()
    decoded = json.loads(json_in)
    for cat1 in decoded['categories']:
        p = Category(cat_id = cat1['id'], short_name = cat1['short_name'])
        p.save()
        
    #return user to now-populated index page
    return HttpResponseRedirect(reverse('events:index'))

#The search/results view
#aka where the magic happens
def search(request):
    #TODO:Fix sorting(?), switch to using template
    #result sorting is marginal for mixed alpha-numeric
    #add searched categories to page
    search_str = ""
    page_count = 0
    num_args = len(request.GET.getlist('cat')) #number of categories chosen
    for_ctr = 0
    result_data = {} #initialize dictionary for relevant info
    
    #build API search string from user choices
    for x in request.GET.getlist('cat'):
        search_str += x
        for_ctr += 1
        if (for_ctr < num_args):
            search_str += ","
    search_str = "https://www.eventbriteapi.com/v3/events/search/?token=A3KV5OGJFN7YWZI6JLIC&categories=" + search_str
    search_str += "&location.address=" + quote_plus(request.GET['address']) + \
                  "&location.within=" + request.GET['within']

    #populate the smaller result_data object from API query
    #there is probably a more efficient way to just grab the complete
    #JSON object of all event data and parse the required data from it
    def Populate(pageno, res_dat):
        decoded = json.loads(urlopen(search_str+"&page="+str(pageno)).read())
        for item in decoded['events']:
            key_str = str(item['id'])
            res_dat[key_str] = {'url':item['url'],
                                    'logo_url':item['logo_url'],
                                    'start_date':item['start']['local'],
                                    'event_name':item['name']['text'],
                                    'city':item['venue']['address']['city'],
                                    'region':item['venue']['address']['region']}
        if (pageno == 1):
            return decoded['pagination']['page_count']
        return

    #populate data from first page and get number of pages back
    page_count = Populate(1, result_data)

    #populate additional result page data
    #this is a bottleneck for large result sets
    #as we go through all results before rendering the
    #search page
    if (page_count > 1):
        for y in range(2, page_count+1):
            Populate(y, result_data)
            
    
    #get static style.css location
    css_url = static('events/style.css')

    #Create string for HTML output
    #proper format viewable in /static/events/initial.html
    response_str = """<!DOCTYPE html>\n<head>
    <!-- Page written by Daniel O'Neill -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/list.js/1.1.1/list.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/list.pagination.js/0.1.1/list.pagination.min.js"></script>
    <!-- list and pagination courtesy of www.listjs.com under MIT License-->
    <link rel="stylesheet" type="text/css" href="{0}">\n</head>\n<body>
    <ul><li><h1>Nearby Events</h1></li></ul>
    <div id="users">
        <ul>\n\t\t\t<li>
                <button class="sort" data-sort="name">Sort by name</button>
                <button class="sort" data-sort="date">Sort by date</button>
                <a href="../"><button class="research">New Search</button></a>\n\t\t\t</li>
        </ul>
        <ul class="paginationTop"></ul>
        <ul class="list">"""

    #update with css url
    response_str = response_str.format(css_url)
    
    #promt for new search if no results
    if not result_data:
        search_again ="""
            <a href="../"><li>No results found, click to search elsewhere</li></a>"""
        response_str += search_again

    else:
        #construct output for each event
        for event in result_data.itervalues():
            lurl = str(event['logo_url'])
            url = str(event['url'])
            city = str(event['city'])
            region = str(event['region'])
            #gracefully displays alternate ascii characters
            #for unicode special characters
            #possibly avoid issues by using pure unicode strings
            ename = event['event_name'].encode(errors='replace')
            datetg = datetime.datetime.strptime(str(event['start_date']), "%Y-%m-%dT%H:%M:%S")
            date = datetg.strftime("%A, %B %d, %Y")
            time = datetg.strftime("%I:%M %p")
            event_str = """\n\t\t\t<a href="{0}">\n\t\t\t\t<li>
                    <img class="logo" src="{1}" onerror="imgError(this);">
                    <h4 class="name">{2}</h4>
                    <h6 class="location">{5}, {6}</h6>
                    <h6 class="date">{3} {4}</h6>         
                </li></a>"""

            #fill in variables in the preceding block
            response_str += event_str.format(url, lurl, ename, date, time, city, region)

    #close out html and add bottom page selection   
    response_str += """
        </ul>
        <ul class="paginationBottom" style="list-style-type:none"></ul>\n\t</div>"""

    # see /events/static/events/events.js
    # for image replacement and page/sort options
    js_url = static('events/events.js')
    js_resp = """\n\t<script src="{0}"></script>\n</body>""".format(js_url)

    #combine created response and JS strings and create page
    return HttpResponse(response_str + js_resp)

