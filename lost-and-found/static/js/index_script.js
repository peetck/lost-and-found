var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
function initialize(){
    axios.get('/post_api/')
    .then(function (response) {
        // handle success
        data = response.data

        posts = data[0]
        pictures = data[1]

        console.log(posts)
        console.log(pictures)

        for (i = 0; i < posts.length; i++){
            url = null
            for (j = 0; j < pictures.length; j++){
                if (pictures[j].post == posts[i].id){
                    url = pictures[j].picture
                }
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
    card.append(createCardBody(title, desc))
    card.append(createCardText(type))
    card.append(createCardFooter(assetType, location, date_time, contact1, contact2, user))

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

function createCardBody(title, desc){
    /*
    <div class="card-body">
        <h5 class="card-title">
            <b>{{ post.title|truncatechars:20 }} </b>
        </h5>
        <p class="card-text">
            <p>{{ post.desc|truncatechars:50 }}</p>
        </p>
    </div>
    */
    let div = document.createElement('div')
    div.setAttribute('class', 'card-body')

    let h5 = document.createElement('h5')
    h5.setAttribute('class', 'card-title')
    h5.innerHTML = '<b>' + truncatechars(title, 20)  + '</b>'

    let p = document.createElement('p')
    p.setAttribute('class', 'card-text')
    p.innerHTML = '<p>' + truncatechars(desc, 50) + '</p>'

    div.append(h5)
    div.append(p)

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
    let msg = (type == 'found' ? 'เจอของหาย' : 'ตามหาของ')
    p.innerHTML = '<span class="badge badge-pill badge-success text-light">' + msg + '</span>'

    div.append(p)

    return div
}

function createCardFooter(assetType, location, date_time, contact1, contact2, user){
    /*
    <div class="card-footer">
        <small class="text-muted">
            <b>ประเภทของสิ่งของ : </b><span id='assetType'>{{ post.assetType }}</span>
            <br>
            <b>สถานที่ : </b><span id='location'> {{ post.location }} </span>
            <br>
            <b>วันและเวลา : </b><span id='date_time'> {{ post.date_time|date:"d/m/Y H:i" }} </span>
            <br>
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
    span1.innerHTML = '<b>ประเภทของสิ่งของ : </b>' + assetType + '<br>'

    let span2 = document.createElement('span')
    span2.innerHTML = '<b>สถานที่ : </b>' + location + '<br>'

    let span3 = document.createElement('span')
    let datetime = new Date(date_time)
    span3.innerHTML = '<b>วันและเวลา : </b>' + ((datetime.getDate() < 10 ? '0' : '') + datetime.getDate()) + '/' + ((datetime.getMonth() + 1 < 10 ? '0' : '') + (datetime.getMonth() + 1)) + '/' +
    datetime.getFullYear() + ' ' + ((datetime.getHours() < 10 ? '0' : '') + datetime.getHours()) + ':' + ((datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes()) + '<br>'

    let span4 = document.createElement('span')
    span4.innerHTML = '<b>เบอร์ติดต่อ : </b>' + contact1 + '<br>'

    let span5 = document.createElement('span')
    span5.innerHTML = '<b>อีเมล์ : </b>' + contact2 + '<br>'

    let span6 = document.createElement('span')
    span6.innerHTML = '<b>โดย : </b>' + user + '<br>'

    small.append(span1)
    small.append(span2)
    small.append(span3)
    small.append(span4)
    small.append(span5)
    small.append(span6)

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