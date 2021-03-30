from flask import Blueprint, request, redirect, url_for, session, flash
from flask.templating import render_template
from muse_app import db
from muse_app.models.user_model import User
from muse_app.models.playlist_model import Playlist
from muse_app.models.recommend_model import Recommend
from muse_app.services import spotipy
from muse_app.utils.song_cluster import get_data
import pandas as pd

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        data = User.query.filter(User.email==email, User.password==password).first() 
        if not data :
            flash("사용자 정보가 없습니다!")
            return redirect(url_for('main.login'))
        else : 
            session['logged_in'] = True
            session['firstname'] = data.first_name
            session['id'] = data.id
            return render_template('search.html', session=session)

@bp.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET','POST'])
def regiter_user():
    if request.method == 'GET':
        return render_template("register.html")
    else :
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        user_email = User.query.filter(User.email==email).first()
        if user_email :
            print(user_email)
            flash("중복된 email!")
            return render_template("register.html")
        else :
            usertable=User(first_name = firstname, last_name = lastname, email = email, password = password) 
            db.session.add(usertable)
            db.session.commit()
            flash("가입 성공!")    
            return redirect(url_for('main.login'))

@bp.route('/search', methods=['GET','POST']) 
def search():
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        return render_template('search.html', session=session)

@bp.route('/search_result', methods=['GET','POST']) 
def search_result():
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        try :
            search = request.form.get('search')
            artists = spotipy.get_artists(search)
            tracks = spotipy.get_tracks(search)
            return render_template('search_result.html', artists=artists, tracks=tracks, session=session)
        except :
            flash("검색값을 입력하세요")
            return redirect(url_for('main.search'))
           
@bp.route('/search_result/<artist>', methods=['GET','POST']) 
def artist_playlist(artist=None) :

     if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
     else :
        tracks = spotipy.get_artist_track(artist)
        return render_template('search_artist_result.html', tracks=tracks, session=session)
   
@bp.route('/playlist', methods=['GET','POST']) 
def playlist():
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            playlist = Playlist.query.filter(Playlist.user_id==session['id']).paginate(page=page, per_page=10)
            return render_template('playlist.html', playlist=playlist, session=session)
        else : 
            tracks = request.form.getlist('tracks')
            for track in tracks :
                track, artist, temp = track.split(',')
                released = temp[0:4]
                playlist = Playlist(track=track, artist=artist, released=released, user_id=session['id'])
                db.session.add(playlist)
            db.session.commit()
            page = request.args.get('page', 1, type=int)
            playlist = Playlist.query.filter(Playlist.user_id==session['id']).paginate(page=page, per_page=10)
            return render_template('playlist.html', playlist=playlist, session=session)

@bp.route('/playlist/<int:playlist_id>')
def delete_playlist(playlist_id=None):
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        play_one = Playlist.query.filter(Playlist.id == playlist_id).first()
        db.session.delete(play_one)
        db.session.commit()
        flash("삭제 완료")
        return redirect(url_for('main.playlist'))

@bp.route('/recommend')
def recommend() :
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    playlist = Playlist.query.filter(Playlist.user_id==session['id']).first()
    if not playlist :
        flash("플레이리스트가 없습니다.")
        return render_template('search.html')
    else :
        is_rec = Recommend.query.filter(Recommend.user_id==session['id']).first()
        if is_rec :
            page = request.args.get('page', 1, type=int)
            recommend_list = Recommend.query.filter(Recommend.user_id==session['id']).paginate(page=page, per_page=10)
            return render_template("recommend.html", recommend_list=recommend_list, session=session)
        else :
            playlist = Playlist.query.filter(Playlist.user_id==session['id']).all()
            to_list = []
            for p in playlist :
                to_list.append({'name':p.track, 'year':int(p.released)})
            recommend_list = spotipy.recommend_songs(to_list, get_data())
            for r in recommend_list :
                recommend = Recommend(track=r['name'], artist=r['artists'], released=r['year'], user_id=session['id'])
                db.session.add(recommend)
            db.session.commit()
            page = request.args.get('page', 1, type=int)
            recommend_list = Recommend.query.filter(Recommend.user_id==session['id']).paginate(page=page, per_page=10)
            return render_template("recommend.html", recommend_list=recommend_list, session=session)
      
@bp.route('/recommend/<int:recommend_id>')
def delete_recommend(recommend_id=None):
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        recommend_one = Recommend.query.filter(Recommend.id == recommend_id).first()
        db.session.delete(recommend_one)
        db.session.commit()
        flash("삭제 완료")
        return redirect(url_for('main.recommend'))

@bp.route('/data.json')
def feature():
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        playlist = Playlist.query.filter(Playlist.user_id==session['id']).all()
        play_mean = spotipy.feature_dict(playlist)
        recommend = Recommend.query.filter(Recommend.user_id==session['id']).all()
        reco_mean = spotipy.feature_dict(recommend)

        mean_dict = dict({'playlist' :play_mean, 'recommend':reco_mean})
        return mean_dict

@bp.route("/graph")
def graph():
    if not session.get('logged_in'):
        flash("로그인을 먼저 해주세요")
        return redirect(url_for('main.login'))
    else :
        return render_template('graph.html')

