from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Musics
import os

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
        username = request.POST.get("username")
        music = request.FILES.get("music")

        if not username or not music:
            messages.error(request, "لطفا مقدار های خواسته شدرو به درستی وارد کنید.")
            return render(request, "new.html", context)

        username = username.strip()

        max_size = 20 * 1024 * 1024
        if music.size > max_size:
            messages.error(request, "حجم فایل نباید بیشتر از 20 مگابایت باشد.")
            return render(request, "new.html", context)

        music_name = music.name
        ext = os.path.splitext(music_name)[1].lower()

        allowed_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".aac"]

        if ext not in allowed_extensions:
            messages.error(request, "لطفا فقط فایل صوتی معتبر آپلود کنید.")
            return render(request, "new.html", context)

        music_name = os.path.splitext(music_name)[0]

        try:
            new_music = Musics.objects.create(
                username=username,
                music_name=music_name,
                music=music
            )
        except Exception:
            messages.error(request, "خطا در آپلود فایل رخ داد.")
            return render(request, "new.html", context)

        return HttpResponseRedirect(reverse("detail", kwargs={"pk": new_music.pk}))

    return render(request, "new.html", context)


def detail_view(request, pk):
    context = {}

    music = Musics.objects.filter(pk=pk).first()

    if not music:
        raise Http404("Music not found")

    context["music"] = music

    return render(request, "one.html", context)