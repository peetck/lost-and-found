var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
function initialize(){
    axios.get('/post_api/')
    .then(function (response) {
        // handle success
        posts = response.data

        for (i = 0; i < posts.length; i++){
            if (posts[i].pictures.length >= 1){
                url =  posts[i].pictures[0].picture
            }
            else{
                url = null;
            }
            createCard(posts[i].id, url, posts[i].title, posts[i].desc, posts[i].type,
                posts[i].assetType, posts[i].location, posts[i].date_time,
                posts[i].contact1, posts[i].contact2, posts[i].user)
        }
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
}

function createCard(id, url, title, desc, type, assetType, location, date_time, contact1, contact2, user){
    let a = document.createElement('a')
    a.setAttribute('class', 'col-lg-3 my-3 text-decoration-none')
    a.setAttribute('href', '/detail/' + id + '/')

    let card = document.createElement('div')
    card.setAttribute('class', 'card h-100 w-100 text-dark mycard')

    card.append(createCardWrapper(url))
    card.append(createCardBody(title, desc, assetType, location, date_time))
    card.append(createCardText(type,))
    card.append(createCardFooter(contact1, contact2, user))

    a.append(card)

    document.getElementById('all_post').append(a)
}

function createCardWrapper(url){
    /*
    <div class="wrapper">
        {% if post.postpicture_set.all|length == 0 %}
            <img class="card-img-top" src="{% static 'images/post_default.gif' %}">
        {% else %}
            <img class="card-img-top" src="{{ post.postpicture_set.all.0.picture.url }}">
        {% endif %}
    </div>
    */
    let div = document.createElement('div')
    div.setAttribute('class', 'wrapper')

    let img = document.createElement('img')
    if (url === null){
        img.setAttribute('src', '/static/images/post_default.gif')
    }
    else{
        img.setAttribute('src', url)
    }
    div.append(img)

    return div
}

function createCardBody(title, desc, assetType, location, date_time){
    /*
    <div class="card-body">
        <h5 class="card-title">
            <b>{{ post.title|truncatechars:20 }}</b>
        </h5>
        <div class="card-text">
            <p>{{ post.desc|truncatechars:15 }}</p>
            <p class='m-0'>
                <small>
                    <b>ประเภทสิ่งของ : </b> <span id='assetType'>{{ post.assetType }}</span>
                </small>
            </p>
            <p class='m-0'>
                <small>
                    <b>สถานที่ : </b> <span id='location'> {{ post.location }} </span>
                </small>
            </p>
            <p class='m-0'>
                <small>
                    <b>วันและเวลา : </b> <span id='date_time'> {{ post.date_time|date:"d/m/Y H:i" }} </span>
                </small>
            </p>
        </div>
    </div>
    */
    let div = document.createElement('div')
    div.setAttribute('class', 'card-body')

    let h5 = document.createElement('h5')
    h5.setAttribute('class', 'card-title')
    h5.innerHTML = '<b>' + truncatechars(title, 20)  + '</b>'

    let cardtext = document.createElement('div')
    cardtext.setAttribute('class', 'card-text')

    let p1 = document.createElement('p')
    p1.innerText = truncatechars(desc, 15)

    let p2 = document.createElement('p')
    p2.setAttribute('class', 'm-0')
    p2.innerHTML = '<small> <b>ประเภทสิ่งของ : </b>' + assetType + '</small>'

    let p3 = document.createElement('p')
    p3.setAttribute('class', 'm-0')
    p3.innerHTML = '<small> <b>สถานที่ : </b>' + location + '</small>'

    let p4 = document.createElement('p')
    p4.setAttribute('class', 'm-0')

    let datetime = new Date(date_time)
    datetime = ((datetime.getDate() < 10 ? '0' : '') + datetime.getDate()) + '/' + ((datetime.getMonth() + 1 < 10 ? '0' : '') + (datetime.getMonth() + 1)) + '/' +
                 datetime.getFullYear() + ' ' + ((datetime.getHours() < 10 ? '0' : '') + datetime.getHours()) + ':' + ((datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes())

    p4.innerHTML = '<small> <b>วันและเวลา : </b>' + datetime + '</small>'

    // append
    cardtext.append(p1)
    cardtext.append(p2)
    cardtext.append(p3)
    cardtext.append(p4)

    div.append(h5)
    div.append(cardtext)

    return div
}

function createCardText(type){
    /*
    <div class="container mb-3 ml-1">
        <p class="card-text">
            <span class="badge badge-pill badge-success text-light">เจอของหาย</span>
        </p>
    </div>
    */

    let div = document.createElement('div')
    div.setAttribute('class', 'container mb-3 ml-1')

    let p = document.createElement('p')
    p.setAttribute('class', 'card-text')
    if (type == 'found'){
        let msg = 'เจอของหาย'
        p.innerHTML = '<span class="badge badge-pill badge-success text-light">' + msg + '</span>'
    }
    else{
        let msg = 'ตามหาของ'
        p.innerHTML = '<span class="badge badge-pill badge-danger text-light">' + msg + '</span>'
    }


    div.append(p)

    return div
}

function createCardFooter(contact1, contact2, user){
    /*
    <div class="card-footer">
        <small class="text-muted">
            <b>เบอร์ติดต่อ : </b> <span id='contact1'> {{ post.contact1 }} </span>
            <br>
            <b>อีเมล์ : </b> <span id='contact2'> {{ post.contact2 }} </span>
            <br>
            <b>โดย : </b> {{ post.user.username }}
        </small>
    </div>
    */

    let div = document.createElement('div')
    div.setAttribute('class', 'card-footer')

    let small = document.createElement('small')
    small.setAttribute('class', 'text-muted')

    let span1 = document.createElement('span')
    span1.innerHTML = '<b>เบอร์ติดต่อ : </b>' + contact1 + '<br>'

    let span2 = document.createElement('span')
    span2.innerHTML = '<b>อีเมล์ : </b>' + contact2 + '<br>'

    let span3 = document.createElement('span')
    span3.innerHTML = '<b>โดย : </b>' + user + '<br>'

    small.append(span1)
    small.append(span2)
    small.append(span3)

    div.append(small)

    return div
}

/* truncatechars function */
function truncatechars(text, lim) {
    if (text.length > lim){
        return text.substring(0, lim - 1) + "...";
    }
    return text;
}

initialize()