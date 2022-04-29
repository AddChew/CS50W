const csrftoken = getCookie('csrftoken')
const Route = ReactRouterDOM.Route
const Router = ReactRouterDOM.BrowserRouter
const Switch = ReactRouterDOM.Switch
const NavLink = ReactRouterDOM.NavLink
const Redirect = ReactRouterDOM.Redirect
const useParams = ReactRouterDOM.useParams


function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}


function Alert(props) {
    return <div class={ props.className }>{ props.error }</div>
}


function Anchor(props) {
    return <NavLink className={ props.className } to={ props.url } exact={ true } onClick={ props.callback }>{ props.url_name }</NavLink>
}


function List(props) {
    return (
        <li class="nav-item">
            <Anchor className={ props.className } url={ props.url } url_name={ props.url_name } callback={ props.callback } />
        </li>
    ) 
}


function Navigation(props) {
    function logout(event) {
        fetch("/api/logout")
        .then(response => response.json())
        .then(result => {
            props.setCredentials({...result})
            window.location.reload()
        })
        event.preventDefault()
    }

    const {logged_in, username} = props.credentials
    return (
        <div>
            <nav class="navbar navbar-expand-lg navbar-light">
                <Anchor className="navbar-brand font-weight-bold" url="#" url_name="Network" />
                <div>
                    <ul class="navbar-nav mr-auto">
                        { logged_in && <List className="nav-link font-weight-bold" url={ `/${username}` } url_name={ username } /> }
                        <List className="nav-link" url="/" url_name="All Posts" />
                        { logged_in && <List className="nav-link" url="/following" url_name="Following" /> }
                        { logged_in &&  <List className="nav-link" url="/logout" url_name="Log Out" callback={ logout }/> }
                        { !logged_in && <List className="nav-link" url="/login" url_name="Log In" /> }
                        { !logged_in && <List className="nav-link" url="/register" url_name="Register" /> }
                    </ul>
                </div>
            </nav>
            <hr></hr>            
        </div>
    )
}


function Login(props) {
    const [error, setError] = React.useState(null)

    React.useEffect(() => document.title = "Social Network - Login", [])

    function login(event) {
        const credentials = {
            username: document.querySelector("[name='username']").value, 
            password: document.querySelector("[name='password']").value
        }
        fetch("/api/login", {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            body: JSON.stringify(credentials)            
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) setError(result.error)
            else {
                props.setCredentials({...result})
                window.location.reload()
            }
        })
        event.preventDefault()
    }

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={ login }>
                { error && <Alert className="alert alert-danger" error={ error } /> }
                <input type="text" name="username" class="form-control form-group" placeholder="Username" required />
                <input type="password" name="password" class="form-control form-group" placeholder="Password" required />
                <input type="submit" class="btn btn-primary" value="Login" /> 
            </form>
            Don't have an account? <Anchor className="" url="/register" url_name="Register here." />            
        </div>
    )
}


function Register(props) {
    const [error, setError] = React.useState({})

    React.useEffect(() => document.title = "Social Network - Register", [])

    function register(event) {
        const credentials = {
            username: document.querySelector("[name='username']").value,
            email: document.querySelector("[name='email']").value,
            password: document.querySelector("[name='password']").value,
            confirmation: document.querySelector("[name='confirmation']").value
        }
        fetch("/api/register", {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            body: JSON.stringify(credentials)            
        })
        .then(response => response.json())
        .then(result => {
            if (result.logged_in) props.setCredentials({...result})
            else setError(parseError(result))
        })
        event.preventDefault()
    }

    function parseError(error) {
        var parsed_error = {}
        Object.entries(error).forEach(([field, error]) => parsed_error[field] = error[0].message)
        return parsed_error
    }

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={ register }>
                { error.username && <Alert className="alert alert-danger" error={ error.username } /> }
                <input type="text" name="username" class="form-control form-group" placeholder="Username" required />
                { error.email && <Alert className="alert alert-danger" error={ error.email } /> }
                <input type="email" name="email" class="form-control form-group" placeholder="Email Address" required />
                { error.__all__ && <Alert className="alert alert-danger" error={ error.__all__ } /> }
                { error.password && <Alert className="alert alert-danger" error={ error.password } /> }
                <input type="password" name="password" class="form-control form-group" placeholder="Password" required />
                <input type="password" name="confirmation" class="form-control form-group" placeholder="Confirm Password" required />
                <input type="submit" class="btn btn-primary" value="Register" />
            </form>
            Already have an account? <Anchor className="" url="/login" url_name="Log In here." />            
        </div>
    )
}


function NewPost(props) {
    const [state, setState] = React.useState({error: null, content: ""})

    function updateContent(event) {
        setState({...state, content: event.target.value})
    }

    function createPost(event) {
        const content = {content: document.querySelector("[name='content']").value}
        fetch("/api/posts/create", {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            body: JSON.stringify(content)             
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                setState({...state, ...result})
            } else {
                var new_posts = [result, ...props.state.posts.map(post => ({...post}))]
                if (new_posts.length === 11) new_posts.pop()
                props.setState({...props.state, posts: new_posts})
                setState({error: null, content: ""})                
            }
        })
        event.preventDefault()
    }

    return (
        <div>
            { state.error && <Alert className="alert alert-danger" error={ state.error } /> }
            <form class="container post-container" onSubmit={ createPost }>
                <h5>New Post</h5>
                <textarea name="content" class="form-control form-group" placeholder="What's happening?" value={ state.content } onChange={ updateContent } required />
                <input type="submit" class="btn btn-primary" value="Post" />                 
            </form>
        </div>
    )
}


function Post(props) {
    const [post, setPost] = React.useState({
        error: null,
        content: null,
        num_likes: null,
        liked: null,
        edit: false
    })

    function likeUnlike() {
        if (props.credentials.logged_in) {
            const body = {like: !post.liked}
            fetch(`/api/posts/${props.post.id}`, {
                method: "PUT",
                headers: {"X-CSRFToken": csrftoken},
                mode: "same-origin",
                body: JSON.stringify(body)                
            })
            .then(response => response.ok ? response : response.json())
            .then(result => {
                if (result.error) setPost({...post, ...result})
                else setPost({...post, num_likes: post.num_likes + (post.liked ? -1 : 1), liked: !post.liked})
            })
        }
    }

    function edit(event) {
        setPost({...post, edit: true})
        event.preventDefault()
    }

    function save(event) {
        const body = {content: event.target.querySelector("[name='content']").value}
        fetch(`/api/posts/${props.post.id}`, {
            method: "PUT",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            body: JSON.stringify(body)
        })
        .then(response => response.ok ? response : response.json())
        .then(result => {
            if (result.error) setPost({...post, error: result.error})
            else setPost({...post, ...body, edit: false})
        })
        event.preventDefault()
    }

    React.useEffect(() => setPost({error: null, content: props.post.content, num_likes: props.post.num_likes, liked: props.post.liked, edit: false}), [props.post])

    return (
        <div>
            { post.error && <Alert className="alert alert-danger" error={ post.error } /> }
            <form class="container post-container" onSubmit={ save }>
                <NavLink className="username" to={ `/${ props.post.owner }`}><h5>{ props.post.owner }</h5></NavLink>
                { post.edit ? <textarea name="content" class="form-control form-group" required>{ post.content }</textarea> : <p>{ post.content }</p>}
                { !post.edit && <p class="text-grey">{ props.post.date_posted }</p>}
                { !post.edit && (
                    <div>
                        <i class={ `fa-heart margin-right ${ post.liked ? "fa-solid red" : "fa-regular"}`} onClick={ likeUnlike }></i>
                        <span class="text-grey">{ post.num_likes }</span>
                    </div>
                ) }
                { props.credentials.username === props.post.owner && (post.edit ? <input type="submit" class="btn btn-primary" value="Save" /> : <NavLink className="margin-right" to="#" onClick={ edit }>Edit</NavLink>) }
            </form>            
        </div>
    )
}


function Posts(props) {
    const [state, setState] = React.useState({error: null, page_num: null, num_pages: null, posts: []})

    React.useEffect(() => document.title = `Social Network - ${props.title}`, [props.title])

    function fetchPosts(event) {
        var input = null
        if (event !== null) {
            event.preventDefault()
            var input = event.target.textContent
        }

        if (input === null || input === undefined) var page_num = 1
        else if (input === "Next") var page_num = state.page_num + 1
        else if (input === "Previous") var page_num = state.page_num - 1
        else var page_num = input

        fetch(`${props.api_url}?page=${page_num}`)
        .then(response => response.json())
        .then(result => {
            if (result.error) setState({...state, error: result.error})
            else setState({...state, ...result})
        })
    }

    React.useEffect(() => fetchPosts(null), [props.title])

    const first_page = state.page_num === 1
    const last_page = state.page_num === state.num_pages
    return (
        <div>
            { (props.title === "All Posts" || props.title === "Following") && <h2>{ props.title }</h2> }
            { (props.title === "All Posts") && props.credentials.logged_in && <NewPost state={ state } setState={ setState } /> }
            <div>
                { state.error && <Alert className="alert alert-danger" error={ state.error } /> }
                { state.posts.length === 0 && <p>No posts to show</p>}
                { state.posts.map(post => <Post post={ post } credentials={ props.credentials }/>)}
                { state.posts.length !== 0 && (
                <nav>
                    <ul class="pagination justify-content-center">
                        <li class={ `page-item ${ first_page ? "disabled" : "" }` }>
                            <a class="page-link" href="#" onClick={ fetchPosts }>Previous</a>
                        </li>
                        { !first_page && <li class="page-item"><a class="page-link" href="#" onClick={ fetchPosts }>{ state.page_num - 1 }</a></li> }
                        <li class="page-item active"><a class="page-link" href="#" onClick={ fetchPosts }>{ state.page_num }</a></li>
                        { !last_page && <li class="page-item"><a class="page-link" href="#" onClick={ fetchPosts }>{ state.page_num + 1 }</a></li> }
                        <li class={ `page-item ${ last_page ? "disabled" : "" }` }>
                            <a class="page-link" href="#" onClick={ fetchPosts }>Next</a>
                        </li>
                    </ul>
                </nav>
                )}                
            </div>
        </div>
    )
}


function Profile(props) {
    const username = useParams().username
    const [profile, setProfile] = React.useState({
        error: null, followed: false, id: null, username: null, num_posts: null, 
        num_followers: null, num_following: null, date_joined: null, posts: [],
        page_num: null, num_pages: null
    })

    React.useEffect(() => document.title = `Social Network - ${profile.error ? profile.error.slice(0, -1) : username}`, [profile.error, profile.username])

    function fetchProfile(event) {
        var input = null
        if (event !== null) {
            event.preventDefault()
            var input = event.target.textContent
        }

        if (input === null || input === undefined) var page_num = 1
        else if (input === "Next") var page_num = profile.page_num + 1
        else if (input === "Previous") var page_num = profile.page_num - 1
        else var page_num = input

        fetch(`/api/${username}?page=${page_num}`)
        .then(response => response.json())
        .then(result => {
            if (result.error) setProfile({...profile, error: result.error})
            else setProfile({...profile, ...result, error: null}) // posts: result.posts.map(post => ({...post}))
        })
    }

    function followUnfollow() {
        if (props.credentials.logged_in && props.credentials.username !== username) {
            const body = {follow: !profile.followed}
            fetch(`/api/${username}`, {
                method: "PUT",
                headers: {"X-CSRFToken": csrftoken},
                mode: "same-origin",
                body: JSON.stringify(body)                 
            })
            .then(response => response.ok ? response : response.json())
            .then(result => {
                if (result.error) setProfile({...profile, error: result.error})
                else setProfile({...profile, ...result, error: null, followed: !profile.followed, num_followers: profile.num_followers + (profile.followed ? -1 : 1)})
            })
        }
    }

    React.useEffect(() => fetchProfile(null), [username])

    const first_page = profile.page_num === 1
    const last_page = profile.page_num === profile.num_pages   
    return (
        <div class="container profile-container">
            { profile.error && <Alert className="alert alert-danger" error={ profile.error } /> }
            { !profile.error && (
            <div class="margin-bottom-2rem">
                <h2>{ profile.username }</h2>
                <div class="form-group">
                    <p class="text-grey">Joined { profile.date_joined }</p>
                    <strong>{ profile.num_posts }</strong><span class="text-grey margin-right-1rem"> Posts</span>
                    <strong>{ profile.num_following }</strong><span class="text-grey margin-right-1rem"> Following</span>
                    <strong>{ profile.num_followers }</strong><span class="text-grey margin-right-1rem"> Followers</span>
                </div>
                { props.credentials.logged_in && props.credentials.username !== username && <input type="submit" class="btn btn-primary" onClick={ followUnfollow } value={ profile.followed ? "Unfollow": "Follow"} /> }
            </div>
            )}
            <div>
                { profile.posts.length === 0 && <p>No posts to show</p>}
                { profile.posts.map(post => <Post post={ post } credentials={ props.credentials }/>)}
                { profile.posts.length !== 0 && (
                <nav>
                    <ul class="pagination justify-content-center">
                        <li class={ `page-item ${ first_page ? "disabled" : "" }` }>
                            <a class="page-link" href="#" onClick={ fetchProfile }>Previous</a>
                        </li>
                        { !first_page && <li class="page-item"><a class="page-link" href="#" onClick={ fetchProfile }>{ profile.page_num - 1 }</a></li> }
                        <li class="page-item active"><a class="page-link" href="#" onClick={ fetchProfile }>{ profile.page_num }</a></li>
                        { !last_page && <li class="page-item"><a class="page-link" href="#" onClick={ fetchProfile }>{ profile.page_num + 1 }</a></li> }
                        <li class={ `page-item ${ last_page ? "disabled" : "" }` }>
                            <a class="page-link" href="#" onClick={ fetchProfile }>Next</a>
                        </li>
                    </ul>
                </nav>
                )}                
            </div>           
        </div>        
    )
}


function App() {
    const [credentials, setCredentials] = React.useState({logged_in: null, username: null})

    function fetchCredentials() {
        fetch("/api/authentication")
        .then(response => response.json())
        .then(credentials => setCredentials({...credentials}))
    }

    React.useEffect(fetchCredentials, [])

    const logged_in = credentials.logged_in
    return (
        <Router>
            <Route path="/" render={() => <Navigation credentials={ credentials } setCredentials={ setCredentials } />}/>
            <Switch>
                <Route path="/" exact render={() => <Posts credentials={ credentials } title="All Posts" api_url="/api/posts" />}/>
                <Route path="/login" render={() => logged_in ? <Redirect to="/" /> : <Login setCredentials={ setCredentials } />} />
                <Route path="/register" render={() => logged_in ? <Redirect to="/" /> : <Register setCredentials={ setCredentials } />} />
                <Route path="/following" render={() => logged_in ? <Posts credentials={ credentials } title="Following" api_url="/api/posts/following" /> : <Redirect to="/" />} />
                <Route path="/:username" render={() => <Profile credentials={ credentials } /> }/>
            </Switch>
        </Router>
    )
}

ReactDOM.render(<App />, document.querySelector("#root"))