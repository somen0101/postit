from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, PostTagList, PostTagName, PostComment
from django.db.models import Count,Q
from django.urls import reverse,reverse_lazy
from . forms import PostForm, CommentModelForm
from django.utils import timezone
from django import forms
from django.views.generic import FormView



def index(request, page=0):
    max_page = Post.objects.count() // 10
    return construct_page(request, PostTagList.objects.values('content_id'), Post.objects.order_by('-upload_date')[page*10:(page+1)*10].values(), page, max_page, 'picture:index')


def construct_page(request, all_content_ids, page_contents, current_page, max_page, url_type, url_word=''):
    contents = []
    for item in page_contents:
        tmp_dict = item
        tmp_dict.update({'tags': PostTagList.objects.filter(content_id=item['id']).select_related('tag')})
        contents.append(tmp_dict)


    tag_cnt = PostTagList.objects.filter(content__in=all_content_ids).values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:10]
    tag_names = [PostTagName.objects.filter(id = item.get('tag'))[0] for item in tag_cnt]
    tags = [{'name': tag_names[i].name, 'count': tag_cnt[i]["tag_count"]} for i in range(len(tag_names))]


    page_list = [{'num':x, 'valid':0 <= x and x <= max_page} for x in range(current_page-5, current_page+4)]


    return render(request, 'picture/index.html', {'tags': tags, 'contents': contents, 'page':{'type':url_type, 'word': url_word, 'current': current_page, 'max': max_page, 'list': page_list}})


def tag(request, tag_name, page=0):

    tag_id = PostTagName.objects.filter(name=tag_name).get().id
    filtered_list = PostTagList.objects.select_related('content').filter(tag=tag_id).order_by('-content__upload_date')

    max_page = filtered_list.count() // 10

    content_list = filtered_list[page*10:(page+1)*10]
    contents = [{'id':item.content.id, 'title':item.content.title, 'text':item.content.text, 'upload_date':item.content.upload_date} for item in content_list]

    return construct_page(request, PostTagList.objects.values('content_id'), contents, page, max_page, 'picture:tag', tag_name)


def search(request, search_word, page=0):
    filtered_list = Post.objects.filter(Q(title__contains=search_word) | Q(text__icontains=search_word)).order_by('-upload_date')
    max_page = filtered_list.count() // 10

    content_list = filtered_list[page * 10:(page + 1) * 10]
    contents = [{'id': item.id, 'title': item.title, 'text':Post.objects.filter(id=item.id)[0].text, 'upload_date':item.upload_date} for item in content_list]

    return construct_page(request, PostTagList.objects.values('content_id'), contents, page, max_page, 'picture:search', search_word)


def search_post(request):
    d = {
        'Search': request.POST.get('Search')
    }
    if d['Search'] != "":
        return HttpResponseRedirect(reverse('picture:search', args=(request.POST['Search'],)))

    return HttpResponseRedirect(reverse('picture:index'))


def topic_create(request):
    template_name = 'picture/create_post.html'
    ctx = {}
    if request.method == 'GET':
        ctx['form'] = PostForm()
        return render(request, template_name, ctx)

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = Post()
            #post_tag = PostTagName()
            #post_tag_list = PostTagList()
            cleaned_data = post_form.cleaned_data
            post.title = cleaned_data['title']
            post.text = cleaned_data['text']
            post.upload_date = timezone.now()
            all_tags = request.POST["tag"]
            all_tags_split = str(all_tags).split("#")
            del all_tags_split[0]
            post.save()
            for t in all_tags_split:
                tags = PostTagName.objects.filter(name=t)
                if len(tags) == 0:
                   PostTagName.objects.create(name=t)
                   PostTagList.objects.create(content=post, tag=PostTagName.objects.filter(name=t).get())
                else:
                   PostTagList.objects.create(content=post, tag=PostTagName.objects.filter(name=t).get())

        return redirect(reverse_lazy('picture:index'))


class TopicAndCommentView(FormView):
    template_name = 'picture/detail_post.html'
    form_class = CommentModelForm

    def form_valid(self, form):
         comment = form.save(commit=False)
         comment.topic = Post.objects.get(id=self.kwargs['pk'])
         comment.no = PostComment.objects.filter(topic=self.kwargs['pk']).count() + 1
         comment.save()
         return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('picture:detail_post', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()

        tag_cnt = PostTagList.objects.filter(content__in=PostTagList.objects.values('content_id')).values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:10]
        tag_names = [PostTagName.objects.filter(id=item.get('tag'))[0] for item in tag_cnt]
        tags = [{'name': tag_names[i].name, 'count': tag_cnt[i]["tag_count"]} for i in range(len(tag_names))]
        ctx['post_tags'] = PostTagList.objects.filter(content_id=self.kwargs['pk'])
        ctx['tags'] = tags
        ctx['topic'] = Post.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = PostComment.objects.filter(topic_id=self.kwargs['pk']).order_by('no')
        return ctx



# Create your views here.
