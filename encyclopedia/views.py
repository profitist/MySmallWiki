import random


from django.shortcuts import render
import markdown
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown_view(request, filename):
    text = util.get_entry(filename)
    if text:
        markdown_text = markdown.markdown(text)
        return render(request, "encyclopedia/article.html", {
            "markdown_text": markdown_text, "page_name": filename})
    return render(request, "encyclopedia/articleNotFound.html", {"page_name": filename})


def search_page(request):
    if request.method == "POST":

        word = request.POST.get('q').lower()

        articles = util.list_entries()
        matches = [article for article in articles if word in article.lower() or article.lower() in word]

        if matches:
            return render(request, "encyclopedia/search_results.html", {"search_results": matches})
        return render(request, "encyclopedia/articleNotFound.html", {"page_name": word})
    return HttpResponseRedirect(reverse("index"))


def create_page(request):
    return render(request, "encyclopedia/page_creator.html", {
        "page_name": '', "redo": False, "content": '', "new_page": True
    })


def save_page(request):
    if request.method == "POST":

        error_path = "encyclopedia/page_creator.html"

        entries_list = util.list_entries()

        create_flag = request.POST.get('creation_flag')
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content')

        if title in entries_list and create_flag == "1":
            return render(request, error_path, {
                "page_name": title, "redo": True, "content": content, "new_page": True})
        util.save_entry(title, content)
        markdown_text = markdown.markdown(content)
        return render(request, "encyclopedia/article.html", {
            "page_name": title, "markdown_text": markdown_text})
    return HttpResponseRedirect(reverse("index"))


def edit_page(request, filename):
    content = util.get_entry(filename)
    return render(request, "encyclopedia/page_creator.html", {
        "page_name": filename,  "content": content, "redo": False, "new_page": False
    })


def random_page(request):
    page_list = util.list_entries()
    page = random.choice(page_list)
    markdown_text = markdown.markdown(util.get_entry(page))
    return render(request, "encyclopedia/article.html", {
        "page_name": page, "markdown_text": markdown_text
    })





