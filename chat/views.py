import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Room
from .forms import EnterRoomForm


def index(request):
    room_uid = request.GET.get('room')
    initial = {}
    room_data = None
    session_data = None
    try:
        room = Room.objects.get(uuid=room_uid)
        room_data = {
            'name': room.name,
            'uid': str(room.uuid)
        }
        initial['room'] = room.name
        session = request.session.get(room.room_key)
        if session:
            session_data = {
                'username': session.get('username', ''),
                'country': session.get('country', '')
            }
            initial.update(session_data)
    except Room.DoesNotExist:
        pass

    form = EnterRoomForm(initial=initial)
    return render(request, 'chat/index.html', {
        'form': form,
        'room': json.dumps(room_data),
        'session': json.dumps(session_data),
        'countries': json.dumps(form.fields['country'].choices)
    })


@require_POST
def enter_room(request):
    data = request.POST
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))

    form = EnterRoomForm(data=data, session=request.session)
    if form.is_valid():
        room = form.save()
        if request.is_ajax():
            return JsonResponse({
                'room': room.get_absolute_url()
            })
        return redirect(room)

    if request.is_ajax():
        return JsonResponse({
            'error': True,
            'message': form.errors['__all__'][0]
        })
    return render(request, 'chat/index.html', {
        'form': form
    })


def room(request, room_uuid):
    room = get_object_or_404(Room, uuid=room_uuid)
    session = request.session.get(room.room_key)
    if session is None:
        return redirect('{}?room={}'.format(
            reverse('index'), room.uuid)
        )
    room_data = {
        'name': room.name,
        'uid': str(room.uuid)
    }
    form = EnterRoomForm()
    return render(request, 'chat/index.html', {
        'room': json.dumps(room_data),
        'session': json.dumps(session),
        'countries': json.dumps(form.fields['country'].choices)
    })
