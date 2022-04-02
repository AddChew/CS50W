const user_email = JSON.parse(document.querySelector("#user-email").textContent)
const logout_url = JSON.parse(document.querySelector("#logout_url").textContent)


class Alert extends React.Component {
    render() {
        return <div class={`alert alert-${ this.props.type }`}>{ this.props.message }</div>
    }
}


class Title extends React.Component {
    render() {
        return <h3>{ this.props.name }</h3>
    }
}


class Heading extends React.Component {
    render() {
        return <div><span class="font-weight-bold">{ this.props.title }: </span>{ this.props.content }</div>
    }
}


class Button extends React.Component {
    render() {
        return <button class="btn btn-sm btn-outline-primary" onClick={ this.props.callback }>{ this.props.name }</button>
    }
}


class Navigation extends React.Component {
    render() {
        const reload = this.props.state.reload ? false : true
        return (
            <div>
                <h2>{ user_email }</h2>
                <Button name="Inbox" callback={ () => this.props.setState({...this.props.state, mailbox: "Inbox", reload: reload, alert: false, prev_mailbox: this.props.state.mailbox}) }/>
                <Button name="Compose" callback={ () => this.props.setState({...this.props.state, mailbox: "Compose", prev_mailbox: this.props.state.mailbox}) }/>
                <Button name="Sent" callback={ () => this.props.setState({...this.props.state, mailbox: "Sent", reload: reload, alert: false, prev_mailbox: this.props.state.mailbox}) }/>
                <Button name="Archived" callback={ () => this.props.setState({...this.props.state, mailbox: "Archive", reload: reload, alert: false, prev_mailbox: this.props.state.mailbox}) }/>
                <a class="btn btn-sm btn-outline-primary" href={ logout_url }>Log Out</a>
                <hr></hr>
            </div>
        )
    }
}


class Mail extends React.Component {
    constructor(props) {
        super(props)
        this.archiveMail = this.archiveMail.bind(this)
        this.replyMail = this.replyMail.bind(this)
    }

    archiveMail() {
        fetch(`/emails/${ this.props.state.mail.id }`, {
            method: "PUT",
            body: JSON.stringify({
                archived: this.props.state.mail.archived ? false : true,
            })
        })
        .then(() => {
            const archive = this.props.state.mail.archived ? "unarchived": "archived"
            this.props.setState({
                ...this.props.state,
                mailbox: "Inbox",
                prev_mailbox: this.props.state.mailbox,
                alert: {message: `Emall has been ${ archive } successfully.`, type: "success"},
            })
        })
    }

    replyMail() {
        this.props.setState({
            ...this.props.state,
            mailbox: "Compose",
            draft: {
                ...this.props.state.draft, 
                recipients: this.props.state.mail.sender, 
                subject: `${this.props.state.mail.subject.startsWith("Re:") ? "" : "Re: "}${ this.props.state.mail.subject }`,
                body: `On ${this.props.state.mail.timestamp} ${this.props.state.mail.sender} wrote: \n${this.props.state.mail.body}`,
            }
        })
    }

    render() {
        const headings = (
            <div class="margin-bottom">
                <Heading title="From" content={ this.props.state.mail.sender } />
                <Heading title="To" content={ this.props.state.mail.recipients.join(", ") } />
                <Heading title="Subject" content={ this.props.state.mail.subject } />
                <Heading title="Timestamp" content={ this.props.state.mail.timestamp } />
            </div>            
        )

        var contents = [headings, <Button name="Reply" callback={ this.replyMail }/>, <hr></hr>, <div>{ this.props.state.mail.body }</div>]

        if (this.props.state.prev_mailbox !== "Sent") {
            contents.splice(2, 0, <Button name={ this.props.state.mail.archived ? "Unarchive" : "Archive" } callback={ this.archiveMail }/>)
        }

        return <div>{ contents }</div>
    }
}


class MailPreview extends React.Component {
    constructor(props) {
        super(props)
        this.viewMail = this.viewMail.bind(this)
    }

    viewMail() {
        fetch(`/emails/${ this.props.mail.id }`, {
            method: "PUT",
            body: JSON.stringify({
                read: true,
            })
        })
        this.props.setState({
            ...this.props.state,
            mailbox: "Mail",
            prev_mailbox: this.props.state.mailbox,
            mail: this.props.mail,
        })
    }

    render() {
        const color = this.props.mail.read ? "background-grey" : ""
        const address = this.props.state.mailbox === "Sent" ? `To: ${ this.props.mail.recipients.join(", ") }` : `From: ${ this.props.mail.sender }`
        return (
            <div class={ `container mail ${ color }` } onClick={ this.viewMail }>
                <div class="row">
                    <div class="col-4 font-weight-bold">{ address }</div>
                    <div class="col-4">{ this.props.mail.subject }</div>
                    <div class="col-4 text-right text-grey">{ this.props.mail.timestamp }</div>
                </div>
            </div>
        )
    }
}


class MailBox extends React.Component {
    fetchMails(mailbox) {
        fetch(`/emails/${ mailbox.toLowerCase() }`)
        .then(response => response.json())
        .then(mails => this.props.setState({
                ...this.props.state,
                prev_mailbox: this.props.state.mailbox,
                mails: mails,
            })
        )
    }

    componentDidMount() {
        this.fetchMails(this.props.state.mailbox)
    }

    componentDidUpdate(prevProps) {
        if (this.props.state.reload !== prevProps.state.reload) {
            this.fetchMails(this.props.state.mailbox)
        }
    }

    render() {
        var contents = [<Title name={ this.props.state.mailbox } />]

        this.props.state.mails.forEach(mail => {
            contents.push(<MailPreview state={ this.props.state } setState={ this.props.setState } mail={ mail }/>)
        })

        return <div>{ contents }</div>
    }
}


class Compose extends React.Component {
    constructor(props) {
        super(props)
        this.sendMail = this.sendMail.bind(this)
        this.updateDraft = this.updateDraft.bind(this)
    }

    sendMail(event) {
        var mail = {
            recipients: document.getElementById("recipients").value,
            subject: document.getElementById("subject").value,
            body: document.getElementById("body").value,
        }
        fetch("/emails", {
            method: "POST",
            body: JSON.stringify(mail),
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                this.props.setState({
                    ...this.props.state,
                    prev_mailbox: this.props.state.mailbox,
                    draft: {...this.props.state.draft, ...mail},
                    alert: {message: result.error, type: "danger"},
                })
            } else {
                this.props.setState({
                    ...this.props.state,
                    mailbox: "Sent",
                    prev_mailbox: this.props.state.mailbox,
                    draft: {...this.props.state.draft, recipients: "", subject: "", body: ""},
                    alert: {message: result.message, type: "success"},
                })
            }
        })
        event.preventDefault()
    }

    updateDraft() {
        this.props.setState({
            ...this.props.state,
            prev_mailbox: this.props.state.mailbox,
            draft: {
                ...this.props.state.draft, 
                recipients: document.getElementById("recipients").value,  
                subject: document.getElementById("subject").value, 
                body: document.getElementById("body").value,
            }
        })
    }

    render() {
        var form = (
            <form onSubmit={ this.sendMail }>
            <div class="form-group">
                From: <input disabled class="form-control" value={ this.props.state.draft.sender } />
            </div>
            <div class="form-group">
                To: <input id="recipients" class="form-control" value={ this.props.state.draft.recipients } onChange={ this.updateDraft } />
            </div>
            <div class="form-group">
                <input class="form-control" id="subject" value={ this.props.state.draft.subject } placeholder="Subject" onChange={ this.updateDraft } />
            </div>
            <div class="form-group">
              <textarea class="form-control" id="body" value={ this.props.state.draft.body } placeholder="Body" onChange={ this.updateDraft } ></textarea>
            </div>
            <input type="submit" class="btn btn-primary"/>
          </form>
        )
        var contents = [<Title name="New Email" />, form]

        return <div>{ contents }</div>
    }
}


class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            mailbox: "Inbox",
            prev_mailbox: "",
            mails: [],
            mail: false,
            draft: {sender: user_email, recipients: "",  subject: "", body: ""},
            alert: false,
            reload: false,
        }
        this.setState = this.setState.bind(this)
    }

    render() {
        var contents = [<Navigation state={ this.state } setState={ this.setState } />]
        if (this.state.alert) {
            contents.push(<Alert type={ this.state.alert.type } message={ this.state.alert.message } />)
        }

        switch(this.state.mailbox) {
            case "Compose":
                contents.push(<Compose state={ this.state } setState={ this.setState } />)
                return contents
            case "Mail":
                contents.push(<Mail state={ this.state } setState={ this.setState } />)
                return contents
            default:
                contents.push(<MailBox state={ this.state } setState={ this.setState } />)
                return contents
        }
    }
}


ReactDOM.render(<App />, document.querySelector("#root"))