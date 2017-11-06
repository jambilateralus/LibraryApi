# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from library_api.models import Member, BurrowedBook, ReservedBook
from . import forms


def get_current_member(req):
    current_user = req.user
    member = Member.objects.filter(user=current_user)
    return member


@login_required
def index(request):
    template = 'home/index.html'
    librarian = request.user.username
    form = forms.MemberIdForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            member_id = form.cleaned_data['memberId']
            member = Member.objects.filter(member_id=member_id)
            if member:
                member_name = member[0].first_name + " " + member[0].last_name
                member_year = str(member[0].registered_year)[:4]
                burrowed_books = BurrowedBook.objects.filter(burrowed_by=member)
                reserved_books = ReservedBook.objects.filter(reserved_by=member)

                # if member exits then show member info page
                return render(request, 'home/member_info.html', {"member_name": member_name,
                                                                "member_year": member_year,
                                                                "burrowed_book_array": burrowed_books,
                                                                "reserved_book_array": reserved_books})
            else:
                # else render index page
                return render(request, template, {"librarian": librarian, 'form': form})

        else:
            # form not valid
            return render(request, template, {"librarian": librarian, 'form': form})

    else:
        # request method is get
        return render(request, template, {"librarian": librarian, 'form': form})


def member_details(request, ):
    template = 'home/memberinfo.html'
    return render(request, template)  #

# def index(request):
#     template = 'home/index.html'
#     member = get_current_member(request)
#     member_name = member[0].first_name + " " + member[0].last_name
#     registered_year = str(member[0].registered_year)
#     burrowed_books = BurrowedBook.objects.filter(burrowed_by=member)
#     requested_book = RequestedBook.objects.filter(requested_by=member)
#
#     return render(request, template, {"burrowed_book_array": burrowed_books,
#                                       "requested_book": requested_book,
#                                       "member_name": member_name,
#                                       "registered_year": registered_year})
