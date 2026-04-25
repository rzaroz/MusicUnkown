from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Musics

def home(request):
    musics = Musics.objects.all().order_by("-pk")
    paginator = Paginator(musics, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"musics": page_obj}
    return render(request, "index.html", context)


def add_new(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username", None)
        music = request.FILES.get("music", None)

        if not username or not music:
            messages.error(request, "لطفا مقدار های خواسته شدرو به درستی وارد کنید.")
            return render(request, "new.html", context)

        music_name = music.name

        allowed_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".aac"]

        if not any(music_name.lower().endswith(ext) for ext in allowed_extensions):
            messages.error(request, "لطفا فقط فایل صوتی معتبر آپلود کنید.")
            return render(request, "new.html", context)

        allowed_content_types = [
            "audio/mpeg",
            "audio/wav",
            "audio/x-wav",
            "audio/ogg",
            "audio/mp4",
            "audio/aac",
        ]

        if music.content_type not in allowed_content_types:
            messages.error(request, "فرمت فایل توسط سرور پشتیبانی نمی‌شود.")
            return render(request, "new.html", context)

        music_name = music_name.split('.')[0]

        new_music = Musics.objects.create(
            username=username,
            music_name=music_name,
            music=music
        )
        new_music.save()

        return HttpResponseRedirect(reverse("detail", kwargs={"pk": new_music.pk}))


    return render(request, "new.html", context)


def detail_view(request, pk):
    context = {}

    music = Musics.objects.filter(pk=pk).first()

    if not music:
        raise Http404("Music not found")

    context["music"] = music

    return render(request, "one.html", context)